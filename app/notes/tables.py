import sqlalchemy as sa
from sqlalchemy import BigInteger, Column, DateTime, Identity, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(BigInteger, Identity(), primary_key=True)
    title = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    tags = Column(JSONB, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=sa.func.now())
