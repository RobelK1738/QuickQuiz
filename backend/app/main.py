from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routers import quizzes 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="QuickQuiz API") 

origins = [
    "http://localhost:3000",  
    "https://quickquizfrontend.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(quizzes.router, prefix="/api/quizzes", tags=["quizzes"])
