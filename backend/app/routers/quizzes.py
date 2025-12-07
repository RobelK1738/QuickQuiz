import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.auth import get_db, get_current_user, get_optional_user
from app.models.models import Quiz, Question, Attempt, User, AttemptAnswer
from app.schemas.quizzes import (
    QuizCreate,
    QuizSummary,
    QuizDetail,
    SubmitAnswers,
    SubmitResult,
    AttemptDetail,
)

router = APIRouter()


def normalize(s: str) -> str:
    return (s or "").strip().lower()


# -----------------------------
# PUBLIC QUIZZES
# -----------------------------
@router.get("", response_model=List[QuizSummary])
def list_public_quizzes(db: Session = Depends(get_db)):
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.is_public == True)
        .order_by(Quiz.created_at.desc())
        .all()
    )
    return quizzes


# -----------------------------
# USER'S QUIZZES
# -----------------------------
@router.get("/my", response_model=List[QuizSummary])
def list_my_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.creator_id == current_user.id)
        .order_by(Quiz.created_at.desc())
        .all()
    )
    return quizzes


# -----------------------------
# CREATE QUIZ
# -----------------------------
@router.post("", response_model=QuizSummary, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_in: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    title = (quiz_in.title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if len(quiz_in.questions) < 1:
        raise HTTPException(status_code=400, detail="At least one question is required")

    quiz = Quiz(
        title=title,
        description=(quiz_in.description or "").strip(),
        creator_id=current_user.id,
        is_public=True,
    )
    db.add(quiz)
    db.flush()

    for idx, q in enumerate(quiz_in.questions):
        qt = (q.text or "").strip()
        ca = (q.correct_answer or "").strip()
        if not qt or not ca:
            raise HTTPException(
                status_code=400,
                detail="Each question and answer must be non-empty",
            )
        db.add(
            Question(
                quiz_id=quiz.id,
                order=idx,
                text=qt,
                correct_answer=ca,
            )
        )

    db.commit()
    db.refresh(quiz)
    return quiz


# -----------------------------
# UPDATE QUIZ
# -----------------------------
@router.put("/{quiz_id}", response_model=QuizSummary)
def update_quiz(
    quiz_id: int,
    quiz_in: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this quiz.",
        )

    title = (quiz_in.title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    if len(quiz_in.questions) < 1:
        raise HTTPException(status_code=400, detail="At least one question is required")

    quiz.title = title
    quiz.description = (quiz_in.description or "").strip()

    db.query(Question).filter(Question.quiz_id == quiz.id).delete()
    for idx, q in enumerate(quiz_in.questions):
        qt = (q.text or "").strip()
        ca = (q.correct_answer or "").strip()
        if not qt or not ca:
            raise HTTPException(
                status_code=400,
                detail="Each question and answer must be non-empty",
            )
        db.add(
            Question(
                quiz_id=quiz.id,
                order=idx,
                text=qt,
                correct_answer=ca,
            )
        )

    db.commit()
    db.refresh(quiz)
    return quiz


# -----------------------------
# MY RESULTS (list)
# -----------------------------
@router.get("/my-results")
def get_my_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempts = (
        db.query(Attempt)
        .join(Quiz, Quiz.id == Attempt.quiz_id)
        .filter(Attempt.user_id == current_user.id)
        .order_by(Attempt.id.desc())
        .all()
    )
    return [
        {
            "id": a.id,
            "quiz_id": a.quiz_id,
            "quiz_title": a.quiz.title if a.quiz else "",
            "score": a.score,
            "total": a.total,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in attempts
    ]


# -----------------------------
# QUIZ DETAIL
# -----------------------------
@router.get("/{quiz_id}", response_model=QuizDetail)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz or (not quiz.is_public and (not current_user or quiz.creator_id != current_user.id)):
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.order.asc())
        .all()
    )
    include_answers = current_user and quiz.creator_id == current_user.id
    questions_payload = [
        {
            "id": q.id,
            "order": q.order,
            "text": q.text,
            "correct_answer": q.correct_answer if include_answers else None,
        }
        for q in questions
    ]

    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "questions": questions_payload,
    }


# -----------------------------
# DELETE QUIZ
# -----------------------------
@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if quiz.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this quiz.",
        )

    db.delete(quiz)
    db.commit()
    return None


# -----------------------------
# SUBMIT QUIZ ANSWERS
# -----------------------------
@router.post("/{quiz_id}/submit", response_model=SubmitResult)
def submit_quiz(
    quiz_id: int,
    submission: SubmitAnswers,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = (
        db.query(Question)
        .filter(Question.quiz_id == quiz.id)
        .order_by(Question.order.asc())
        .all()
    )

    answer_lookup = {
        a.question_id: (a.answer or "").strip()
        for a in submission.answers
    }

    results: list[dict] = []
    score = 0

    for q in questions:
        user_answer = answer_lookup.get(q.id, "")
        is_correct = normalize(user_answer) == normalize(q.correct_answer)
        if is_correct:
            score += 1
        results.append(
            {
                "question_id": q.id,
                "question": q.text,
                "user_answer": user_answer,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
            }
        )

    # save attempt
    attempt = Attempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        total=len(questions),
        details=results,  # backup JSON payload
    )
    db.add(attempt)
    db.flush()

    # save per-question answers
    for res in results:
        db.add(
            AttemptAnswer(
                attempt_id=attempt.id,
                question_id=res["question_id"],
                user_answer=res["user_answer"],
                is_correct=res["is_correct"],
            )
        )

    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "quiz_title": attempt.quiz.title,
        "score": score,
        "total": len(questions),
        "results": results,
        "created_at": attempt.created_at.isoformat() if attempt.created_at else None,
    }


# -----------------------------
# ATTEMPT DETAIL (for viewing past results)
# -----------------------------
@router.get("/attempts/{attempt_id}", response_model=AttemptDetail)
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id)
        .options(
            joinedload(Attempt.quiz),
            joinedload(Attempt.answers).joinedload(AttemptAnswer.question),
        )
        .first()
    )

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    if attempt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this attempt",
        )

    results: list[dict] = []

    # 1️⃣ Prefer AttemptAnswer rows
    if attempt.answers:
        for aa in attempt.answers:
            q = aa.question
            results.append(
                {
                    "question_id": aa.question_id,
                    "question": q.text if q else "",
                    "user_answer": aa.user_answer,
                    "correct_answer": q.correct_answer if q else "",
                    "is_correct": aa.is_correct,
                }
            )

    # 2️⃣ Fallback to `details` JSON (for old attempts)
    elif attempt.details:
        details = attempt.details
        if isinstance(details, str):
            try:
                details = json.loads(details)
            except Exception:
                details = []
        for r in details or []:
            results.append(
                {
                    "question_id": r.get("question_id"),
                    "question": r.get("question", ""),
                    "user_answer": r.get("user_answer", ""),
                    "correct_answer": r.get("correct_answer", ""),
                    "is_correct": r.get("is_correct", False),
                }
            )

    # 3️⃣ Final fallback: at least return the questions
    if not results:
        questions = (
            db.query(Question)
            .filter(Question.quiz_id == attempt.quiz_id)
            .order_by(Question.order.asc())
            .all()
        )
        for q in questions:
            results.append(
                {
                    "question_id": q.id,
                    "question": q.text,
                    "user_answer": "",
                    "correct_answer": q.correct_answer,
                    "is_correct": False,
                }
            )

    return {
        "attempt_id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "quiz_title": attempt.quiz.title if attempt.quiz else "",
        "score": attempt.score,
        "total": attempt.total,
        "results": results,
        "created_at": attempt.created_at.isoformat() if attempt.created_at else None,
    }

# -----------------------------
# LAST ATTEMPT
# -----------------------------
@router.get("/{quiz_id}/my-latest-attempt")
def get_my_latest_attempt(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempt = (
        db.query(Attempt)
        .filter(Attempt.quiz_id == quiz_id, Attempt.user_id == current_user.id)
        .order_by(Attempt.created_at.desc())
        .first()
    )

    if not attempt:
        return {"attempted": False}

    return {
        "attempted": True,
        "attempt_id": attempt.id,
        "score": attempt.score,
        "total": attempt.total,
        "completed_at": attempt.created_at.isoformat() if attempt.created_at else None,
    }
