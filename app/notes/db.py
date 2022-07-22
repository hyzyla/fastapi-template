import sqlalchemy as sa

from app import db
from app.notes import models as m
from app.notes import tables as t


def select_note(note_id: int) -> m.Note | None:
    """Get single note by ID"""

    query = sa.select(t.Note).where(t.Note.id == note_id)
    row = db.select_one(query)
    return m.Note.from_orm(row) if row else None


def select_notes() -> list[m.Note]:
    """Get list of notes ordered by date created"""

    rows = db.select_all(sa.select(t.Note).order_by(t.Note.created_at.desc()))
    return [m.Note.from_orm(row) for row in rows]


def insert_note(note: m.NoteCreate) -> m.Note:
    row = db.select_one(
        sa.insert(t.Note)
        .values(
            title=note.title,
            text=note.text,
            tags=note.tags,
        )
        .returning(t.Note)
    )
    return m.Note.from_orm(row)


def update_note(note_id: int, note: m.NoteUpdate) -> None:
    db.execute(
        sa.update(t.Note)
        .values(
            title=note.title,
            text=note.text,
            tags=note.tags,
        )
        .where(t.Note.id == note_id)
    )
