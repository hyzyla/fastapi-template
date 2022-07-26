# FastAPI template

Features:
* FastAPI
* Synchronous code (is easier to write than async one)
* docker / docker-compose development setup
* SQLAlchemy Core, with 1.4 style
* Simple work with SQLAlchemy connection, using contextvars
* Codebase divided by domains
* Three layer of abstractions: handlers, services, storages
* mypy, black, isort, flake8
* poetry
* Sentry
* pytest: examples of tests, fixtures and factories
* typer for commands

## Handler example

./app/notes/handlers
```python
router = APIRouter(prefix="/notes", tags=["notes"])

@router.post(path="", response_model=Note)
def create_note(note: NoteCreate) -> Note:

    with db.begin():
        _note = services.create_note(note)

    return _note
```

./app/notes/services.py
```python
def create_note(note: NoteCreate) -> Note:
    """Save note into database"""

    logger.info("Creating new note", extra={"note": note.dict()})

    _note = db.insert_note(note)
    return _note
```

./app/notes/db.py
```python
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
```

./app/notes/models.py
```python
class NoteBase(BaseModel):
    title: str
    text: str
    tags: list[str] = Field(default_factory=list)


class NoteCreate(NoteBase):
    ...


class Note(NoteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

## Project structure
```
├── app
│   ├── commands
│   │   └── __main__.py
│   ├── health
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── migrations
│   │   ├── versions
│   │   │   └── 2022-07-21_add_notes_table_1c9c682bb2ed.py
│   │   ├── README
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── notes
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── handlers.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── tables.py
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── error_reporting.py
│   ├── errors.py
│   ├── main.py
│   ├── setup.py
│   ├── types.py
│   └── utils.py
├── scripts
│   ├── init.sh
│   ├── lint-check.sh
│   ├── lint.sh
│   ├── start.dev.sh
│   ├── start.sh
│   ├── test.sh
│   └── upgrade-db.sh
├── tests
│   ├── notes
│   │   ├── __init__.py
│   │   ├── factories.py
│   │   └── test_notes_handlers.py
│   ├── __init__.py
│   └── conftest.py
├── Dockerfile
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.yaml
├── poetry.lock
└── pyproject.toml
```

## Run project

Use docker-compose:

```shell
docker-compose up app
```

## Tools

### Update or add new package

1.  Use command:

```shell
docker-compose run --rm poetry add {package}
```

or

```shell
poetry add {package}
```

2.  (optionally) Rebuild docker containers:

```shell
docker-compose build
```

### Run tests

```shell
docker-compose run --rm test
```

### Database migration

*   autogenerate migration

```shell
docker-compose run --rm alembic-autogenerate "Migration message"
```

*   upgrade to latest version

```shell
docker-compose run --rm alembic upgrade heads
```

*   upgrade to previous version

```shell
docker-compose run --rm alembic downgrade -1
```

### Linters & Formatters

```shell
docker-compose run --rm lint
```

If you want to run separately black, flake8 or other tool use \_base service:

```shell
docker-compose run --rm _base black --help
```
