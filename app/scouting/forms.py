from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, SelectField, BooleanField, IntegerRangeField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ScoutingDataForm(FlaskForm):

    position = IntegerField(validators=[DataRequired()])
    match_number = IntegerField(validators=[DataRequired()])

    name = StringField("Scouter Name", validators=[DataRequired()])

    auto_notes = IntegerField("Notes scored", default=0)
    auto_pickup = IntegerField("Number of notes picked up", default=0)

    tele_notes = IntegerField("Notes scored", default=0)

    tele_from_subwoofer = BooleanField("Scored in subwoofer")
    tele_from_podium = BooleanField("Scored from podium")
    tele_from_wing = BooleanField("Scored from wing")
    tele_from_center = BooleanField("Scored from center")

    climb = SelectField("Climb", validators=[], choices=[
        ("single", "Single climb"),
        ("harmonized", "Harmonized"),
        ("parked", "Parked"),
        ("no-attempt", "Not attempted"),
        ("failed", "Attempted but failed")
    ])


    intake_preference = SelectField("Intake Preference", validators=[], choices=[
        ("ground", "Ground"),
        ("source", "Source"),
        ("both", "Both")
    ])

    disabled = SelectField("Was Disabled", validators=[], choices=[
        ("no", "No"),
        ("part", "Yes - Part of match"),
        ("yes", "Yes - Full match")
    ])

    driver_confidence = IntegerRangeField("Driver Confidence", default=0)
    defence_rating = IntegerRangeField("Defence Rating", default=0)

    comments = TextAreaField("Comments - GP", validators=[])

    submit = SubmitField("Save")