import sqlalchemy as sa
from pydantic_factories import ModelFactory

from app import db
from app.notes import models as m
from app.notes import tables as t


class NoteFactory(ModelFactory[m.Note]):
    __model__ = m.Note

    @classmethod
    def create_sync(cls, **kwargs) -> m.Note:
        instance = cls.build(**kwargs)
        return cls.save(instance)

    @staticmethod
    def save(instance: m.Note) -> m.Note:
        with db.begin():
            query = sa.insert(t.Note).values(instance.dict()).returning(t.Note)
            row = db.select_one(query)
            return m.Note.from_orm(row)

    @classmethod
    def get_note(cls, note_id: int) -> m.Note | None:
        with db.connect():
            row = db.select_one(sa.select(t.Note).where(t.Note.id == note_id))
            return m.Note.from_orm(row) if row else None
