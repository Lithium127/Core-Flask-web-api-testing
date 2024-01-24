from __future__ import annotations
import typing as t

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class CRUDMixin(object):
    id: Mapped[int] = mapped_column(primary_key = True)

    def save(self, commit: bool = True) -> CRUDMixin:
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
    
    

db = SQLAlchemy(model_class=Base)