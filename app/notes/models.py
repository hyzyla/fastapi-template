from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str
    text: str
    tags: list[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    ...


class NoteUpdate(NoteBase):
    ...


class Note(NoteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Notes(BaseModel):
    notes: list[Note]
