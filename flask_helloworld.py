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
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from forms import RegistrationForm
from forms import LoginForm
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Generate some posts
# ===========================================================================
posts = [
    {'author': 'Andres Potapczynski',
     'title': 'Blog Post 1',
     'content': 'Blah blah',
     'date_posted': '2019-04-09'},
    {'author': 'Liliana Pineda',
     'title': 'Blog Post 2',
     'content': 'Blah',
     'date_posted': '2019-04-10'}
]
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Create the functionality
# ===========================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bishop2891'


@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!',
              'success')
        return redirect(url_for('hello'))
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
# Run the instance
# ===========================================================================


if __name__ == '__main__':
    app.run(debug=True)
# ===========================================================================
