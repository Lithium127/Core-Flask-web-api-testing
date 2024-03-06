from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateNewCompetitionForm(FlaskForm):
    event_code = StringField(
        "Event Code", 
        validators=[DataRequired(), Length(4, message="Event code must be more than 4 characters")]
    )
    year = IntegerField(
        "Year", 
        validators=[DataRequired()]
    )
    event_type = SelectField(
        "Event Type", 
        validators=[DataRequired()], 
        choices=[("qual", "Quals"),("playoff", "Playoffs")]
    )

class RequestFieldYearForm(FlaskForm):
    year = DateField("Target Year", validators=[DataRequired()])
    submit = SubmitField("Fetch")