# ===========================================================================
# Documentation
# ===========================================================================
"""

"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import DateField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Content
# ===========================================================================


class RegistrationForm(FlaskForm):
    first_name = StringField(label='First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField(label='Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField(label='Address',
                          validators=[DataRequired(), Length(min=2, max=20)])
    city = StringField(label='City',
                       validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField(label='State',
                        validators=[DataRequired(), Length(min=2, max=20)])
    zipcode = IntegerField(label='Zipcode', validators=[DataRequired()])

    country = StringField(label='Country',
                          validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField(label='Phone',
                        validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField(label='Birth Date', validators=[DataRequired()])

    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Sign Up')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = True if username.data == 'aaa' else False
        # TODO: add actual SQL query for this
        if user:
            raise ValidationError('That first_name is already taken!')


class LoginForm(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign Up')
# ===========================================================================
