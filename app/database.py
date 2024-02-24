from __future__ import annotations
import typing as t

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import select

class Base(DeclarativeBase):
    pass

class CRUDMixin(object):
    id: Mapped[int] = mapped_column(primary_key = True)

    def add(self) -> CRUDMixin:
        db.session.add(self)
        return self

    def save(self) -> CRUDMixin:
        self.add()
        db.session.commit()
        return self
    

db = SQLAlchemy()