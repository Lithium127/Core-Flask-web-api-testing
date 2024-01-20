from __future__ import annotations
import typing as t

from app.database import db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class GameMatch(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    report: Mapped[t.List[Report]] = relationship(back_populates="gamematch")



class Report(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    gamematch_id: Mapped[int] = mapped_column(ForeignKey("Model.id"))
    gamematch: Mapped[GameMatch] = relationship(back_populates="report")

    team_number: Mapped[int] = mapped_column() # convert to relationship with team
    # team: Mapped[Team] = relationship()
    position: Mapped[int] = mapped_column()

    reporter: Mapped[str] = mapped_column()

    

    comments: Mapped[str] = mapped_column()