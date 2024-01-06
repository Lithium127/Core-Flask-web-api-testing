from app.database import db
from sqlalchemy.orm import Mapped, mapped_column


class Match(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)