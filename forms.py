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
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField(label='Sign Up')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = True if username.data == 'aaa' else False
        # TODO: add actual SQL query for this
        if user:
            raise ValidationError('That username is already taken!')


class LoginForm(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign Up')
# ===========================================================================
