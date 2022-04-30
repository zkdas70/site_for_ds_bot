from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField('Заголовок', validators=[DataRequired()])
    task = TextAreaField("Задание")
    answer = TextAreaField("Ответ")
    coins = FloatField('Баллы за ответ (число)')
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
