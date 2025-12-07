from pydantic import BaseModel, Field
from typing import List, Optional


class SubmittedAnswer(BaseModel):
    question_id: int
    answer: str = ""

class QuestionCreate(BaseModel):
    text: str
    correct_answer: str

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionCreate] = Field(min_items=1, max_items=10)

class QuizSummary(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True

class QuestionOut(BaseModel):
    id: int
    order: int
    text: str
    correct_answer: Optional[str] = None

    class Config:
        from_attributes = True

class QuizDetail(BaseModel):
    id: int
    title: str
    description: Optional[str]
    questions: List[QuestionOut]

    class Config:
        from_attributes = True

class SubmitAnswers(BaseModel):
    answers: List[SubmittedAnswer]

class AnswerResult(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool

class SubmitResult(BaseModel):
    attempt_id: Optional[int] = None
    quiz_id: Optional[int] = None
    quiz_title: Optional[str] = None
    score: int
    total: int
    results: List[AnswerResult]


class AttemptListItem(BaseModel):
    id: int
    quiz_id: int
    quiz_title: str
    score: int
    total: int
    created_at: Optional[str] = None

class AttemptAnswerOut(BaseModel):
    question_id: int
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool

class AttemptDetail(BaseModel):
    attempt_id: int
    quiz_id: int
    quiz_title: str
    score: int
    total: int
    created_at: Optional[str] = None
    results: List[AttemptAnswerOut]
