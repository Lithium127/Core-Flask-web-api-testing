from __future__ import annotations
import typing as t

from app.database import db

from sqlalchemy.orm import Mapped, mapped_column

# TBA Documentation: https://www.thebluealliance.com/apidocs/v3 

class Team(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    # weather the team is using this system for scouting, use for login method?
    is_scouting: Mapped[bool] = mapped_column()

    def __init__(self, team_number: int, **kwargs) -> None:

        # check if team numbr can exist
        if team_number <= 0 or team_number > 9999:
            raise ValueError("Team number out of possible range")
        
        # attempt to make a request to TheBlueAlliance.com to pull team name from their db
        team_name = "[PLACEHOLDER]"

        super(Team, self).__init__(id = team_number, name=team_name, **kwargs)
    
    @classmethod
    def from_tba(cls, team_number: int) -> Team:
        """Creates a team object from a tba profile

        Args:
            team_number (int): The team number of the team

        Returns:
            Team: A team object with tba data
        """
        team = cls.__new__(Team)

        team.id = team_number

        return team
    

    def get_tba_profile(self) -> t.Optional[dict[str,t.Any]]:
        """Makes a request to TBA API and returns the 

        Returns:
            dict[str,t.Any]: The application/json response from tba as a dict
        """
        return {}
    
