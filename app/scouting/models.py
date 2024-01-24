from __future__ import annotations
import typing as t

from datetime import date

from flask import current_app

from app.database import db, CRUDMixin


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if t.TYPE_CHECKING:
    from app.teams.models import Team

class GameMatch(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[date] = mapped_column(default=current_app.config.get("CURRENT_YEAR")())

    report: Mapped[t.List[Report]] = relationship(back_populates="gamematch")


class DataTranslation(db.Model, CRUDMixin):
    id: Mapped[int] = mapped_column(primary_key=True)

    fiscal_year: Mapped[int] = mapped_column(ForeignKey('game_match.year'))

    column_key: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()

    data_type: Mapped[str] = mapped_column()

    @classmethod
    def add_keys(cls, values: dict[str, t.Union[bool, str, int]]) -> None:
        {
            "auto_speaker_score": 1,
            "auto_amp_score": 0,
            "speaker_score": 1,
            "amp_score": 1,
            "coop_point": bool,
            "other_data": "test"
        }

        all_int = []
        all_bool = []
        all_str = []

        # Parse dict into seperate values
        for key in values.keys():
            v = values[key]
            if type(v) == int:
                all_int.append(key)
            elif type(v) == bool:
                all_bool.append(key)
            elif type(v) == str:
                all_str.append(key)
        
        rows = []

        for l in [all_bool, all_int, all_str]:
            rows.append(())
    
    def __init__(self, ) -> None:
        super().__init__()

        



class Report(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    gamematch_id: Mapped[int] = mapped_column(ForeignKey("game_match.id"))
    gamematch: Mapped[GameMatch] = relationship()
    
    reporter: Mapped[str] = mapped_column()

    team_number: Mapped[int] = mapped_column() # convert to relationship with team
    # team: Mapped[t.Optional[Team]] = relationship()
    position: Mapped[int] = mapped_column()
    
    dynamic_data: Mapped[ReportData] = relationship(back_populates='report')

    comments: Mapped[str] = mapped_column()

    def __init__(self, reporter_name, position, team_number, data: dict[str, t.Union[str, bool, int]], comments: str = "") -> None:
        self.reporter = reporter_name
        self.position = position
        self.team_number = team_number
        self.comments = comments

        # here's where data needs to reference the translation table to see where to put each value
        for key in data.keys():
            test = key



class ReportData(db.Model):
    """
    This is a class that contains all dynamic data for each report
    Each row of this table contains values without context, and a parent report
    The data names can be decoded using the 'translation' table
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    report_id: Mapped[int] = mapped_column(ForeignKey('report.id'))
    report: Mapped[Report] = relationship(back_populates='dynamic_data')


    # # Boolean Fields
    # b00: Mapped[t.Optional[bool]] = mapped_column()
    # b01: Mapped[t.Optional[bool]] = mapped_column()
    # b02: Mapped[t.Optional[bool]] = mapped_column()
    # b03: Mapped[t.Optional[bool]] = mapped_column()
    # b04: Mapped[t.Optional[bool]] = mapped_column()
    # b05: Mapped[t.Optional[bool]] = mapped_column()
    # b06: Mapped[t.Optional[bool]] = mapped_column()
    # b07: Mapped[t.Optional[bool]] = mapped_column()
    # b08: Mapped[t.Optional[bool]] = mapped_column()
    # b09: Mapped[t.Optional[bool]] = mapped_column()
    # b10: Mapped[t.Optional[bool]] = mapped_column()
    # b11: Mapped[t.Optional[bool]] = mapped_column()
    # b12: Mapped[t.Optional[bool]] = mapped_column()
    # b13: Mapped[t.Optional[bool]] = mapped_column()
    # b14: Mapped[t.Optional[bool]] = mapped_column()

    # # String Fields
    # s00: Mapped[t.Optional[str]] = mapped_column()
    # s01: Mapped[t.Optional[str]] = mapped_column()
    # s02: Mapped[t.Optional[str]] = mapped_column()
    # s03: Mapped[t.Optional[str]] = mapped_column()
    # s04: Mapped[t.Optional[str]] = mapped_column()
    # s05: Mapped[t.Optional[str]] = mapped_column()
    # s06: Mapped[t.Optional[str]] = mapped_column()
    # s07: Mapped[t.Optional[str]] = mapped_column()
    # s08: Mapped[t.Optional[str]] = mapped_column()
    # s09: Mapped[t.Optional[str]] = mapped_column()

    # # Integer Fields
    # i00: Mapped[t.Optional[str]] = mapped_column()
    # i01: Mapped[t.Optional[str]] = mapped_column()
    # i02: Mapped[t.Optional[str]] = mapped_column()
    # i03: Mapped[t.Optional[str]] = mapped_column()
    # i04: Mapped[t.Optional[str]] = mapped_column()
    # i05: Mapped[t.Optional[str]] = mapped_column()
    # i06: Mapped[t.Optional[str]] = mapped_column()
    # i07: Mapped[t.Optional[str]] = mapped_column()
    # i08: Mapped[t.Optional[str]] = mapped_column()
    # i09: Mapped[t.Optional[str]] = mapped_column()
    # i10: Mapped[t.Optional[str]] = mapped_column()
    # i11: Mapped[t.Optional[str]] = mapped_column()
    # i12: Mapped[t.Optional[str]] = mapped_column()
    # i13: Mapped[t.Optional[str]] = mapped_column()
    # i14: Mapped[t.Optional[str]] = mapped_column()
    # i15: Mapped[t.Optional[str]] = mapped_column()
    # i16: Mapped[t.Optional[str]] = mapped_column()
    # i17: Mapped[t.Optional[str]] = mapped_column()
    # i18: Mapped[t.Optional[str]] = mapped_column()
    # i19: Mapped[t.Optional[str]] = mapped_column()

    def auto_add_value(self, value):
        
        if type(value) == int:
            pass