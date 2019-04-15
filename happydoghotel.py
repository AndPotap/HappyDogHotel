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
app.config['SECRET_KEY'] = 'Bishop2891'
conn = DBConnection()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        conn.insert_into_users_from_form(form=form)
        flash(f'Account created for {form.first_name.data}!',
              'success')
        return redirect(url_for('home'))
    return render_template(template_name_or_list='register.html',
                           form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template(template_name_or_list='login.html',
                           form=form)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Run the server
# ===========================================================================


if __name__ == '__main__':
    app.run(debug=True)
# ===========================================================================
