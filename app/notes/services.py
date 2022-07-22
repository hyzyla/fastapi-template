import logging

from app.errors import DoesNotExistsError
from app.notes import db
from app.notes.models import Note, NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)


def get_notes() -> list[Note]:
    """Get list of notes"""

    return db.select_notes()


def get_note(note_id: int) -> Note:
    """Get note by ID, if note not exists raise error"""

    note = db.select_note(note_id=note_id)
    if not note:
        raise DoesNotExistsError("Note doesn't not exists")
    return note


def create_note(note: NoteCreate) -> Note:
    """Save note into database"""

    logger.info("Creating new note", extra={"note": note.dict()})

    _note = db.insert_note(note)
    return _note


def update_note(note_id: int, note: NoteUpdate) -> Note:
    """Update whole note in database"""

    logger.info("Update note", extra={"note": note.dict(), "note_id": note_id})

    db.update_note(note_id=note_id, note=note)
    _note = get_note(note_id=note_id)
    return _note
