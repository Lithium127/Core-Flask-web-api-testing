from app.database import db

from sqlalchemy.orm import Mapped, mapped_column



class Team(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def __init__(self, team_number: int) -> None:
        super(Team)