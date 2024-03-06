from __future__ import annotations
import typing as t


from datetime import date, datetime
import contextlib

from flask import current_app

from app.database import db, CRUDMixin

from app.frc_api import api


from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

if t.TYPE_CHECKING:
    from app.teams.models import Team

class Competitions(db.Model, CRUDMixin):
    """Table that contains the match schedule for a target event, as well as
    

    Args:
        db (_type_): _description_
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(default=lambda: date.today().year)

    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()

    name: Mapped[str] = mapped_column()

    gamematch: Mapped[t.List[GameMatch]] = relationship(back_populates='comp')

    # def __init__(self, *args, **kwargs) -> None:
    #     super(Competitions, self).__init__(*args, **kwargs)

    @classmethod
    def create_from_frc(cls, event_code: str, tournament_level: str = "playoff", year: t.Optional[int] = None) -> Competitions:

        instance = cls()

        if year is not None:
            instance.year = year
        
        schedule = api.EventSchedule(event_code=event_code, year=instance.year, tournament_level=tournament_level)
        event_data = api.Events(year = instance.year, event_code = event_code).json["Events"][0]
        
        instance.gamematch = []

        for match_ in schedule.schedule:
            instance.gamematch.append(GameMatch.from_frc_report(match_))
        
        instance.start_date = datetime.strptime(event_data["dateStart"], "%Y-%m-%dT%H:%M:%S").date() # 2024-03-06T00:00:00
        instance.end_date = datetime.strptime(event_data["dateEnd"], "%Y-%m-%dT%H:%M:%S").date()

        instance.name = event_data["name"]
        
        return instance
    
    @classmethod
    def create_from_event(cls, event: api.EventSchedule) -> Competitions:
        instance = cls()
        instance.year = event.year
        
        event_data = api.Events(year = instance.year, event_code = event.event_code).json["Events"][0]
        instance.gamematch = []
        for match_ in event.schedule:
            instance.gamematch.append(GameMatch.from_frc_report(match_))
        
        instance.start_date = datetime.strptime(event_data["dateStart"], "%Y-%m-%dT%H:%M:%S").date() # 2024-03-06T00:00:00
        instance.end_date = datetime.strptime(event_data["dateEnd"], "%Y-%m-%dT%H:%M:%S").date()

        instance.name = event_data["name"]
        
        return instance
        


class GameMatch(db.Model, CRUDMixin):
    """A table that contains information for each match in the competition
    Contains 6 reports that hold information for each team in the match
    """
    id: Mapped[int] = mapped_column(primary_key=True)

    comp_id: Mapped[int] = mapped_column(ForeignKey('competitions.id'))
    comp: Mapped[Competitions] = relationship()
    
    match_number: Mapped[int] = mapped_column()
    match_level: Mapped[str] = mapped_column()
    

    reports: Mapped[t.Optional[t.List[Report]]] = relationship(back_populates="gamematch")

    def __init__(self) -> None:
        super(GameMatch, self).__init__()

    def _add_reports(self, teams: list[dict[str,t.Any]]) -> None:
        self.reports = []
        for index in range(len(teams)):
            team = teams[index]
            pos = int(team["station"][-1]) if "Red" not in team["station"] else int(team["station"][-1]) + 3
            self.reports.append(
                Report(
                    None,
                    position = pos,
                    team_number = str(team["teamNumber"]),
                    data={}
                )
            )
    
    @classmethod
    def from_frc_report(cls, match_: dict[str, t.Any]) -> GameMatch:
        instance = GameMatch()
        instance.match_number = int(match_["matchNumber"])
        instance.match_level = match_["tournamentLevel"]
        instance._add_reports(match_["teams"])
        return instance

    
    def add_report(self, report: Report, commit: bool = True) -> None:
        """Adds a report to the report list usnig the report's position attribute
        overwrites old report.


        Args:
            report (Report): Report object to store
            commit (bool, optional): Weather to commit. Defaults to True.
        """
        self.reports[report.position] = report

        if commit:
            self.save()
            


class DataTranslation(db.Model, CRUDMixin):
    id: Mapped[int] = mapped_column(primary_key=True)

    fiscal_year: Mapped[int] = mapped_column(default=lambda: date.today().year)

    column_key: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()

    def __init__(self, column_key: str, title: str):
        super(DataTranslation, self).__init__()
        
        self.column_key = column_key
        self.title = title

    def __repr__(self) -> str:
        return f"<DataTranslation col={self.column_key} title={self.title}>"

    def __str__(self) -> str:
        return f"<DataTranslation col={self.column_key} title={self.title}>"
    

    @classmethod
    def add_keys(cls, values: dict[str, t.Union[bool, str, int]]) -> None:
        """Creates rows in database from a dict, this initially populates the translation table
        The method uses the current year for adding objects and does not yet do data validation so repeat
        title can exist

        Example data : {
            "bool_01":bool,
            "bool_02":True,
            "int_01":int,
            "int_02":0,
            "str_01":str,
            "str_02":""
        }

        Args:
            values (dict[str, t.Union[bool, str, int]]): A dict containing either types of values that rows will be generated from
        """
        all_int = ["i"]
        all_bool = ["b"]
        all_str = ["s"]

        # Parse dict into seperate values
        for key in values.keys():

            v = values[key]

            # get the type of data that will be stored at this value and add the key to its assigned list
            if type(v) == int or v == int:
                all_int.append(key)
            elif type(v) == bool or v == bool:
                all_bool.append(key)
            elif type(v) == str or v == str:
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



class ReportData(db.Model, CRUDMixin):
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

    def set_values_from_dict(self, values: dict[str, t.Union[bool, str, int, None]]) -> None:
        """Sets the data values for a specified ReportData row from a dictionary.
        References DataTranslation table with each key in dict to find specified
        location for each value

        Args:
            values (dict[str, bool | str | int | None]): Values to populate the row with
        """
        stmt = select(DataTranslation).where(DataTranslation.fiscal_year == date.today().year)
        cols = db.session.scalars(stmt).all()

        with contextlib.suppress(AttributeError, KeyError): # 
            for dt in cols:
                value = values.get(dt.title, None)
                
                if value is None:
                    continue

                self.__setattr__(dt.column_key, value)
        
        return self
    
    def values(self) -> dict[str, t.Any]:
        """Returns a dict containing all values in the instanced table row
        example:
        {
            <row_title>:<value>
        }
        
        rather than
        {
            "b01":<value>
        }

        Returns:
            dict[str, t.Any]: Row titles and their tied values
        """
        data = {}
        stmt = select(DataTranslation).where(DataTranslation.fiscal_year == date.today().year)
        cols = db.session.scalars(stmt).all()
        
        for dt in cols:
            value = self.__dict__.get(dt.column_key, None)
            data[dt.title] = value
        return data


        


class Report(db.Model, CRUDMixin):
    """A report object that contains constant header data for each report."""
    id: Mapped[int] = mapped_column(primary_key=True)

    gamematch_id: Mapped[int] = mapped_column(ForeignKey("game_match.id"))
    gamematch: Mapped[GameMatch] = relationship(back_populates="reports")
    
    reporter: Mapped[t.Optional[str]] = mapped_column()

    team_number: Mapped[t.Optional[int]] = mapped_column() # convert to relationship with team
    # team: Mapped[t.Optional[Team]] = relationship()
    position: Mapped[int] = mapped_column()
    
    dynamic_data: Mapped[t.Optional[ReportData]] = relationship(back_populates='report')

    comments: Mapped[str] = mapped_column(default="")

    def __init__(self, reporter_name, position, team_number, data: dict[str, t.Union[str, bool, int, None]], comments: str = "") -> None:
        self.reporter = reporter_name
        self.position = position
        self.team_number = team_number
        self.comments = comments

        # here's where data needs to reference the translation table to see where to put each value
        self.dynamic_data = ReportData().set_values_from_dict(data)
    

    @classmethod
    def __new__(cls, *args, **kwargs) -> Report:
        instance = super().__new__(cls)
        return instance
    
    def dynamic_from_dict(self: Report, data: dict) -> None:
        #with contextlib.suppress(Exception):
        if self.dynamic_data is None:
            self.dynamic_data = ReportData()
        self.dynamic_data.set_values_from_dict(data)
        