from __future__ import annotations
import typing as t

from datetime import date

from flask import current_app

from app.database import db, CRUDMixin


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, and_

if t.TYPE_CHECKING:
    from app.teams.models import Team

class GameMatch(db.Model, CRUDMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(default=lambda: date.today().year)

    reports: Mapped[t.Optional[t.List[Report]]] = relationship(back_populates="gamematch")

    def __init__(self) -> None:
        self._add_reports()

    def _add_reports(self) -> None:
        self.reports = []
        for pos in range(1,7):
            self.reports.append(
                Report(
                    None,
                    pos,
                    None,
                    {}
                )
            )
            


class DataTranslation(db.Model, CRUDMixin):
    id: Mapped[int] = mapped_column(primary_key=True)

    fiscal_year: Mapped[int] = mapped_column(default=lambda: date.today().year)

    column_key: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()

    def __init__(self, column_key: str, title: str):
        super(DataTranslation, self).__init__()
        
        self.column_key = column_key
        self.title = title


    @classmethod
    def add_keys(cls, values: dict[str, t.Union[bool, str, int]]) -> None:
        all_int = ["i"]
        all_bool = ["b"]
        all_str = ["s"]

        # Parse dict into seperate values
        for key in values.keys():

            v = values[key]

            # get the type of data that will be stored at this value and add the key to its assigned list
            if type(v) == int:
                all_int.append(key)
            elif type(v) == bool:
                all_bool.append(key)
            elif type(v) == str:
                all_str.append(key)
        

        for type_list in [all_bool, all_int, all_str]:
            type_prefix = type_list.pop(0) # get target type from the first entry in the current list
            counter = 0

            for entry_key in type_list:
                # format counter such that it will always be 2 digits (ex: 'b01' or b'14')
                formatted_counter = str(counter) if len(str(counter)) == 2 else f"0{str(counter)[0]}"
                # create and save an row that contains translation data for this table
                cls(str(type_prefix + formatted_counter), entry_key).save()
                
                counter += 1 # increment the counter



class ReportData(db.Model):
    """
    This is a class that contains all dynamic data for each report
    Each row of this table contains values without context, and a parent report
    The data names can be decoded using the 'translation' table
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    report_id: Mapped[int] = mapped_column(ForeignKey('report.id'))
    report: Mapped[Report] = relationship(back_populates='dynamic_data')

    year: Mapped[int] = mapped_column(default=lambda: date.today().year)


    # Boolean Fields
    b00: Mapped[t.Optional[bool]] = mapped_column()
    b01: Mapped[t.Optional[bool]] = mapped_column()
    b02: Mapped[t.Optional[bool]] = mapped_column()
    b03: Mapped[t.Optional[bool]] = mapped_column()
    b04: Mapped[t.Optional[bool]] = mapped_column()
    b05: Mapped[t.Optional[bool]] = mapped_column()
    b06: Mapped[t.Optional[bool]] = mapped_column()
    b07: Mapped[t.Optional[bool]] = mapped_column()
    b08: Mapped[t.Optional[bool]] = mapped_column()
    b09: Mapped[t.Optional[bool]] = mapped_column()
    b10: Mapped[t.Optional[bool]] = mapped_column()
    b11: Mapped[t.Optional[bool]] = mapped_column()
    b12: Mapped[t.Optional[bool]] = mapped_column()
    b13: Mapped[t.Optional[bool]] = mapped_column()
    b14: Mapped[t.Optional[bool]] = mapped_column()

    # String Fields
    s00: Mapped[t.Optional[str]] = mapped_column()
    s01: Mapped[t.Optional[str]] = mapped_column()
    s02: Mapped[t.Optional[str]] = mapped_column()
    s03: Mapped[t.Optional[str]] = mapped_column()
    s04: Mapped[t.Optional[str]] = mapped_column()
    s05: Mapped[t.Optional[str]] = mapped_column()
    s06: Mapped[t.Optional[str]] = mapped_column()
    s07: Mapped[t.Optional[str]] = mapped_column()
    s08: Mapped[t.Optional[str]] = mapped_column()
    s09: Mapped[t.Optional[str]] = mapped_column()

    # Integer Fields
    i00: Mapped[t.Optional[str]] = mapped_column()
    i01: Mapped[t.Optional[str]] = mapped_column()
    i02: Mapped[t.Optional[str]] = mapped_column()
    i03: Mapped[t.Optional[str]] = mapped_column()
    i04: Mapped[t.Optional[str]] = mapped_column()
    i05: Mapped[t.Optional[str]] = mapped_column()
    i06: Mapped[t.Optional[str]] = mapped_column()
    i07: Mapped[t.Optional[str]] = mapped_column()
    i08: Mapped[t.Optional[str]] = mapped_column()
    i09: Mapped[t.Optional[str]] = mapped_column()
    i10: Mapped[t.Optional[str]] = mapped_column()
    i11: Mapped[t.Optional[str]] = mapped_column()
    i12: Mapped[t.Optional[str]] = mapped_column()
    i13: Mapped[t.Optional[str]] = mapped_column()
    i14: Mapped[t.Optional[str]] = mapped_column()
    i15: Mapped[t.Optional[str]] = mapped_column()
    i16: Mapped[t.Optional[str]] = mapped_column()
    i17: Mapped[t.Optional[str]] = mapped_column()
    i18: Mapped[t.Optional[str]] = mapped_column()
    i19: Mapped[t.Optional[str]] = mapped_column()

    def set_value(self, key, value) -> None:
        location = db.session.query(DataTranslation.column_key).filter(
            and_(
                DataTranslation.fiscal_year == date.today().year,
                DataTranslation.title == key
            )
        )
        print(location)



class Report(db.Model, CRUDMixin):
    id: Mapped[int] = mapped_column(primary_key=True)

    gamematch_id: Mapped[int] = mapped_column(ForeignKey("game_match.id"))
    gamematch: Mapped[GameMatch] = relationship(back_populates="reports")
    
    reporter: Mapped[t.Optional[str]] = mapped_column()

    team_number: Mapped[t.Optional[int]] = mapped_column() # convert to relationship with team
    # team: Mapped[t.Optional[Team]] = relationship()
    position: Mapped[int] = mapped_column()
    
    dynamic_data: Mapped[t.Optional[ReportData]] = relationship(back_populates='report')

    comments: Mapped[str] = mapped_column(default="")

    def __init__(self, reporter_name, position, team_number, data: dict[str, t.Union[str, bool, int]], comments: str = "") -> None:
        self.reporter = reporter_name
        self.position = position
        self.team_number = team_number
        self.comments = comments

        # here's where data needs to reference the translation table to see where to put each value
        for key in data.keys():
            test = key
    

    @classmethod
    def __new__(cls, *args, **kwargs) -> Report:
        instance = super().__new__(cls)
        return instance