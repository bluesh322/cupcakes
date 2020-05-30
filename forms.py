from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddCupcakeForm(FlaskForm):

    flavor = StringField("Flavor", validators=[InputRequired()])
    size = StringField("Size", validators=[InputRequired()])
    rating = FloatField("Rating", validators=[InputRequired()])
    image = StringField("Image", validators=[Optional(), URL()])