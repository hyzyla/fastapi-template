from http import HTTPStatus

import pytest
from dirty_equals import IsDatetime, IsInt

from tests.notes.factories import NoteFactory

GET_NOTES_API = "/api/notes"
GET_NOTE_API = "/api/notes/{id}"
CREATE_NOTE_API = "/api/notes"


def test_get_notes(client):

    note = NoteFactory.create_sync()

    response = client.get(GET_NOTES_API)
    assert response.status_code == HTTPStatus.OK, response.json()
    response_json = response.json()
    assert response_json == {
        "notes": [
            {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "tags": note.tags,
                "created_at": IsDatetime(approx=note.created_at, iso_string=True),
            }
        ]
    }


def test_get_note(client):

    note = NoteFactory.create_sync()

    response = client.get(GET_NOTE_API.format(id=note.id))
    assert response.status_code == HTTPStatus.OK, response.json()
    response_json = response.json()
    assert response_json == {
        "id": note.id,
        "title": note.title,
        "text": note.text,
        "tags": note.tags,
        "created_at": IsDatetime(approx=note.created_at, iso_string=True),
    }


def test_get_note_not_exists(client):

    response = client.get(GET_NOTE_API.format(id=1))
    assert response.status_code == HTTPStatus.NOT_FOUND, response.json()
    response_json = response.json()
    assert response_json == {"message": "Note doesn't not exists"}


@pytest.mark.parametrize(
    "body, expected",
    [
        # without tags
        (
            {"title": "test title", "text": "Test text"},
            {
                "id": IsInt(),
                "title": "test title",
                "text": "Test text",
                "tags": [],
                "created_at": IsDatetime(iso_string=True),
            },
        ),
        # with tags
        (
            {"title": "test title", "text": "Test text", "tags": ["tag1", "tag2"]},
            {
                "id": IsInt(),
                "title": "test title",
                "text": "Test text",
                "tags": ["tag1", "tag2"],
                "created_at": IsDatetime(iso_string=True),
            },
        ),
    ],
)
def test_create_note(client, body, expected):

    response = client.post(CREATE_NOTE_API, json=body)
    assert response.status_code == HTTPStatus.OK, response.json()
    response_json = response.json()
    assert response_json == expected
    note = NoteFactory.get_note(note_id=response_json["id"])
    assert note.dict() == expected
