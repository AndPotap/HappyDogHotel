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
# from forms import RegistrationForm
# from flask import redirect
# from flask import url_for
# from flask import flash
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Create the associated URLs
# ===========================================================================
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('about.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f'Account created for {form.username.data}!',
#               'success')
#         return redirect(url_for('hello'))
#     return render_template(template_name_or_list='register.html',
#                            form=form)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Run the server
# ===========================================================================


if __name__ == '__main__':
    app.run(debug=True)
# ===========================================================================
