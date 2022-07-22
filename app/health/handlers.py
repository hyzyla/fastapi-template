import sqlalchemy as sa
from fastapi import APIRouter

from app import db
from app.types import StrDict

router = APIRouter(tags=["system"])


@router.get(path="/health")
def health() -> StrDict:

    with db.connect() as conn:
        conn.execute(sa.text("SELECT 1 = 1;"))

    return {"status": "alive"}
