import datetime
from itertools import product

from fastapi import HTTPException
from sqlalchemy import Column, Integer, DateTime

from app.database import Base


class CustomBaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(tz=datetime.timezone.utc))

    def save(self, db):
        db.add(self)
        try:
            db.commit()
        except Exception:
            HTTPException(status_code=400, detail="Failed to save object into database.")
        return product
