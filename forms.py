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
from wtforms import FloatField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import DateField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
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

    phone = StringField(label='Phone',
                        validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField(label='Birth Date', validators=[DataRequired()])

    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    submit = SubmitField(label='Sign Up')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = True if username.data == 'aaa' else False
        # TODO: add actual SQL query for this
        if user:
            raise ValidationError('That first_name is already taken!')


class DogRegistrationForm(FlaskForm):
    # User credentials
    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    # Dog information
    dog_name = StringField(label='Dog Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    breed = StringField(label='Breed',
                        validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField(label='Gender',
                         validators=[DataRequired(), Length(min=1, max=1)])
    color = StringField(label='Color',
                        validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField(label='Birth Date', validators=[DataRequired()])
    brand = StringField(label='Food Brand',
                        validators=[DataRequired(), Length(min=2, max=20)])
    # Submit changes
    submit = SubmitField(label='Sign Up Dog')


class ReservationForm(FlaskForm):
    # User credentials
    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    # Dog information
    dog_name = StringField(label='Dog Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    # Dates information
    date_from = DateField(label='From', validators=[DataRequired()])
    date_to = DateField(label='To', validators=[DataRequired()])

    # Room information
    room_type = IntegerField(label='Room Type', validators=[DataRequired()])

    # Submit changes
    submit = SubmitField(label='Make Reservation')


class RoomPriceForm(FlaskForm):
    # Manager credentials
    email = StringField(label='Manager Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Manager Password', validators=[DataRequired()])

    # Room information
    room_price = FloatField(label='New Price', validators=[DataRequired()])

    room_type = IntegerField(label='Room Type', validators=[DataRequired()])

    # Submit changes
    submit = SubmitField(label='Submit Price Changes')


class EmployeeRegistrationForm(FlaskForm):
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

    phone = StringField(label='Phone',
                        validators=[DataRequired(), Length(min=2, max=20)])
    hired_date = DateField(label='Hired Date', validators=[DataRequired()])

    # Manager Credentials
    email = StringField(label='Manager Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Manager Password', validators=[DataRequired()])

    submit = SubmitField(label='Sign Up Employee')


class LoginForm(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    submit = SubmitField(label='Sign Up')
# ===========================================================================
