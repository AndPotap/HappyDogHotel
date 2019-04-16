# ===========================================================================
# Documentation
# ===========================================================================
"""
This script contains all the URLs for the Happy Dog Hotel Web app
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
from flask import Flask
from flask import render_template
from forms import RegistrationForm
from forms import LoginForm
from forms import DogRegistrationForm
from forms import EmployeeRegistrationForm
from forms import ReservationForm
from forms import RoomPriceForm
from flask import redirect
from flask import url_for
from flask import flash
from Utils.DBConnection import DBConnection
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Create the associated URLs
# ===========================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Intro2DBap3635'
# When running on VM
run_on_instance = input('Run on instance?')
if run_on_instance == 'yes':
    password_db = input('Provide Password')
    instance = True
    db = DBConnection(instance=instance, password=password_db)
else:
    instance = False
    db = DBConnection()
# TODO: need to improve connection to DB (open and close)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db.insert_into_users_from_form(form=form)
        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template(template_name_or_list='register.html', form=form)


@app.route('/register/dog', methods=['GET', 'POST'])
def register_dog():
    form = DogRegistrationForm()
    if form.validate_on_submit():
        db.insert_into_dogs_from_form(form=form)
        flash(f'Account created for {form.dog_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template(template_name_or_list='register_dog.html', form=form)


@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    form = ReservationForm()
    if form.validate_on_submit():
        found_room = db.insert_booking_from_form(form=form)
        if found_room:
            return redirect(url_for('home'))
        else:
            flash('No room for that period! Please check other room type or'
                  'dates', 'error')
    return render_template(template_name_or_list='reserve.html', form=form)


@app.route('/room/price', methods=['GET', 'POST'])
def room_price():
    form = RoomPriceForm()
    if form.validate_on_submit():
        email, password = form.email.data, form.password.data
        if email == 'ap3635@gmail.com' and password == 'ap3635':
            db.update_room_type_price_with_form(form=form)
            return redirect(url_for('home'))
    return render_template(template_name_or_list='room_price.html', form=form)


@app.route('/register/employee', methods=['GET', 'POST'])
def register_employee():
    form = EmployeeRegistrationForm()
    if form.validate_on_submit():
        email, password = form.email.data, form.password.data
        if email == 'ap3635@gmail.com' and password == 'ap3635':
            db.insert_employee_from_form(form=form)
            return redirect(url_for('home'))
    return render_template(template_name_or_list='register_employee.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template(template_name_or_list='login.html', form=form)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Run the server
# ===========================================================================


if __name__ == '__main__':
    if instance:
        app.run(debug=False)
    else:
        app.run(debug=True)
# ===========================================================================
