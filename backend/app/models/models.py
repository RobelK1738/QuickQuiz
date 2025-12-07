from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=True)
    picture = Column(String, nullable=True)

    quizzes = relationship("Quiz", back_populates="creator")
    attempts = relationship("Attempt", back_populates="user")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)

    creator = relationship("User", back_populates="quizzes")
    questions = relationship("Question", cascade="all, delete-orphan", back_populates="quiz")
    attempts = relationship("Attempt", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    order = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")


# app/models/models.py
class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, default=0)
    total = Column(Integer, default=0)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="attempts")

    answers = relationship(
        "AttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(
        Integer,
        ForeignKey("attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_answer = Column(String, nullable=False, default="")
    is_correct = Column(Boolean, default=False)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question")
