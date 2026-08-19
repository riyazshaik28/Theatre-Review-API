from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    created_at: datetime = Field(default_factory=datetime.now)


class ReviewCreate(SQLModel):
    play_name: str = Field(min_length=1)
    reviewer_name: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1)


class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: str
    created_at: datetime


class ReviewUpdate(SQLModel):
    play_name: Optional[str] = Field(default=None, min_length=1)
    reviewer_name: Optional[str] = Field(default=None, min_length=1)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = Field(default=None, min_length=1)