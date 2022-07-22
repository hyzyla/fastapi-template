from fastapi import APIRouter, Body, Path

from app import db
from app.notes import services
from app.notes.models import Note, NoteCreate, Notes, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(path="", response_model=Notes)
def get_notes() -> Notes:

    with db.connect():
        notes = services.get_notes()

    return Notes(notes=notes)


@router.get(path="/{id}", response_model=Note)
def get_note(note_id: int = Path(alias="id")) -> Note:

    with db.connect():
        note = services.get_note(note_id=note_id)

    return note


@router.post(path="", response_model=Note)
def create_note(note: NoteCreate) -> Note:

    with db.begin():
        _note = services.create_note(note)

    return _note


@router.put(path="/{note_id}", response_model=Note)
def update_note(
    note_id: int = Path(alias="id"),
    note: NoteUpdate = Body(...),
) -> Note:

    with db.begin():
        _note = services.update_note(note_id=note_id, note=note)

    return _note
