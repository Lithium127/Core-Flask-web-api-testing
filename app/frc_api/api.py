from __future__ import annotations
import typing as t

import requests
from datetime import date

from flask import current_app



class BaseRequest(object):

    DEFAULT_ENDPOINT = "https://frc-api.firstinspires.org/v3.0/"
    REQUIRED_HEADERS = {
        "Authorization": None, # need to defer call to config for until we have app context
        "If-Modified-Since": ""
    }

    path: str
    method: str

    data: dict
    headers: dict

    response: requests.Response

    def __init__(self, path: str = "", method: str = "GET", data: dict = {}, headers: dict = {}) -> None:
        
        self.REQUIRED_HEADERS["Authorization"] = f"Basic {current_app.config.get('FRC_API_ENCODED_KEY', None)}"
        
        self.path = path
        self.method = method
        self.data = data
        self.headers = headers

        self._make_request()

    def _make_request(self) -> None:
        response = requests.request(
            self.method, 
            f"{self.DEFAULT_ENDPOINT}{self.path}",
            data = self.data,
            headers = self.REQUIRED_HEADERS | self.headers
        )
        # catch errors and process response
        
        self.response = response
    
    @property
    def status(self) -> int:
        return self.response.status_code


class RootCall(BaseRequest):

    def __init__(self) -> None:
        super(RootCall, self).__init__(
            "",
            method="GET",
            data={},
            headers={}
        )

class SeasonSummary(BaseRequest):
    
    def __init__(self, year: t.Optional[int]) -> None:
        if year is None:
            year = date.today().year

        super(SeasonSummary, self).__init__(path = str(year))

