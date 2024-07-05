from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import boto3

DATABASE_URL = "YOUR DATA BASE URL "

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

app = FastAPI()

#  models
class Book(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

class Review(BaseModel):
    book_id: int
    user_id: int
    review_text: str
    rating: int


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.post("/books/", response_model=Book)
async def create_book(book: Book, db: Session = Depends(get_db)):
    async with engine.connect() as conn:
        await conn.execute(
            insert(Book).values(
                title=book.title,
                author=book.author,
                genre=book.genre,
                year_published=book.year_published,
                summary=book.summary
            )
        )
    return book
