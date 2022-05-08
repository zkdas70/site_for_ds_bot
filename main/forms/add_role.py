from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired


class RolesForm(FlaskForm):
    name_role = StringField('Название:', validators=[DataRequired()])
    cost_role = FloatField("Цена:", validators=[DataRequired()])
    submit = SubmitField('Применить')
