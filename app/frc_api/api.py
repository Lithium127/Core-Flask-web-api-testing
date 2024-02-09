from __future__ import annotations
import typing as t

import requests
from datetime import date

from flask import current_app

class FRCAPIError(Exception):
    pass


class BaseRequest(object):
    """Contains common methods for API Call
    Each call subclasses this object and make its call on __init__, storing the response.
    """

    DEFAULT_ENDPOINT = "https://frc-api.firstinspires.org/v3.0/"
    REQUIRED_HEADERS = {
        "Authorization": None, # need to defer call to config for until we have app context
        "If-Modified-Since": ""
    }

    path: str
    method: str

    data: dict
    headers: dict

    _response: requests.Response
    json: dict

    def __init__(self, path: str = "", method: str = "GET", data: dict = {}, headers: dict = {}, defer: bool = False) -> None:
        """Creates request object and collects data from FRC API

        Args:
            path (str, optional): Target API path. Defaults to "".
            method (str, optional): HTTP Method for request. Defaults to "GET".
            data (dict, optional): Data body for request. Defaults to {}.
            headers (dict, optional): Additional request headers. Defaults to {}.
            defer (bool, optional): If the object should defer _make_request, requiring the method to be called seperately. Defaults to False.
        """
        self.REQUIRED_HEADERS["Authorization"] = f"Basic {current_app.config.get('FRC_API_ENCODED_KEY', None)}"
        
        self.path = path
        self.method = method
        self.data = data
        self.headers = headers
        
        if not defer:
            self._make_request()

    def _make_request(self) -> None:
        """Makes a request from the instance URL to the FRC API

        Raises:
            FRCAPIError: Erro from FRC API request
        """
        response = requests.request(
            self.method, 
            f"{self.DEFAULT_ENDPOINT}{self.path}",
            data = self.data,
            headers = self.REQUIRED_HEADERS | self.headers
        )
        # catch errors and process response
        
        self._response = response

        if self.response is None:
            raise FRCAPIError("Request returned NoneType object")
        
        if self.status != 200:
            raise FRCAPIError(f"Error {self.status}")
        self.json = response.json()
        
    @property
    def status(self) -> int:
        """Status code from request"""
        return self.response.status_code
    
    @property
    def response(self) -> requests.Response:
        if self._response is None:
            raise FRCAPIError("Response is None")
        return self._response


class RootCall(BaseRequest):
    """A call to the root FRC API URL, used for checking API status"""

    def __init__(self) -> None:
        super(RootCall, self).__init__(
            "",
            method="GET",
            data={},
            headers={}
        )

class SeasonSummary(BaseRequest):
    """Returns a high level glance of a particular FRC season."""
    
    def __init__(self, year: t.Optional[int] = None) -> None:
        """High level glance of a specified FRC season

        Args:
            year (int, optional): Target year, defaults to current year
        """
        if year is None:
            year = date.today().year

        super(SeasonSummary, self).__init__(path = str(year))

class EventSchedule(BaseRequest):
    """Returns the match schedule for the desired tournament level of a particular
    event in a particular season.
    """

    def __init__(
        self, 
        event_code: str, 
        year: t.Optional[int] = None, 
        tournament_level: t.Optional[str] = None, 
        team_number: t.Optional[int] = None, 
        *, 
        start: t.Optional[int] = None, 
        end: t.Optional[int] = None
    ) -> None:
        """Returns the match schedule for a specific event from event code

        Args:
            event_code (str): The FRC event code
            year (int, optional): Target year. Defaults to current year.
            tournament_level (str, optional): Target match levels, either 'qual' or 'playoffs'. Defaults to 'qual'.
            start (int, optional): Search start index. Defaults to None.
            end (int, optional): Search end index. Defaults to None.
            team_number (int, optional): Team number to search for. Currently defunct.
        """
        
        if year is None:
            year = date.today().year
        
        url_data_keys = [
            (tournament_level, "tournamentLevel"),
            (team_number, "teamNumber"),
            (start, "start"),
            (end, "end")
        ]
        
        path = f"{year}/schedule/{event_code}"
        
        for url_data in url_data_keys:
            if url_data[0] is not None:
                if "?" not in path:
                    path = path + "?"
                path = f"{path}{url_data[1]}={url_data[0]}"
        
        super(EventSchedule, self).__init__(path=path)
    
    @classmethod
    def quals(cls, event_code: str, year: t.Optional[int] = None) -> EventSchedule:
        """Creates an EventSchedule containing the qualification matches from a specified year

        Args:
            event_code (str): Target FRC event code
            year (int, optional): Target year. Defaults to current year.

        Returns:
            EventSchedule: Instance containing data from 'qual'
        """
        instance = EventSchedule(event_code, year=year, tournament_level="qual")
        return instance

    @classmethod
    def playoff(cls, event_code: str, year: t.Optional[int] = None) -> EventSchedule:
        """Creates an EventSchedule containing the playoff matches from a specified year

        Args:
            event_code (str): Target FRC event code
            year (int, optional): Target year. Defaults to current year.

        Returns:
            EventSchedule: Instance containing data from 'playoff'
        """
        instance = EventSchedule(event_code, year=year, tournament_level="playoff")
        return instance

    @property
    def schedule(self) -> dict[str, t.Any]:
        """Event schedule"""
        return self.json["Schedule"]


class Events(BaseRequest):
    event_list: list[dict]
    event_count: int
    
    def __init__(
        self, 
        year: t.Optional[int] = None,
        event_code: t.Optional[str] = None,
        team_number: t.Optional[int] = None,
        district_code: t.Optional[int] = None,
        exclue_district: t.Optional[bool] = None,
        week_number: t.Optional[int] = None,
        tournement_type: t.Optional[str] = None
    ) -> None:
        
        if year is None:
            year = date.today().year
            
        path = f"{year}/events?"
        
        url_data_keys = [
            (event_code, "eventCode"),
            (team_number, "teamNumber"),
            (district_code, "districtCode"),
            (exclue_district, "excludeDistrict"),
            (week_number, "weekNumber"),
            (tournement_type, "tournamentType")
        ]
        
        for url_data in url_data_keys:
            if url_data[0] is not None:
                path = f"{path}{url_data[1]}={url_data[0]}"
        
        print(f"{self.DEFAULT_ENDPOINT}{path}")

        super(Events, self).__init__(path=path)
        
        self.event_count = self.json["eventCount"]
        self.event_list = self.json["Events"]


class Team(BaseRequest):
    info: dict
    
    def __init__(self, team_number: int, *, year: t.Optional[int] = None) -> None:
        if year is None:
            year = date.today().year
        
        
        super(Team, self).__init__(path=f"{year}/teams?teamNumber={team_number}")
        
        self.info = self.json["teams"][0]