from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField
from wtforms.validators import DataRequired


class AdForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    salary = FloatField('Зарплата', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')
