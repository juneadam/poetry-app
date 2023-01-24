"""server for poetry app"""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """render the homepage"""

    return render_template('homepage.html')

@app.route('/sign-up')
def user_sign_up():
    """render a sign-up page where the user can create an account"""

    return render_template('signup.html')

@app.route('/login')
def user_login():
    """check user credentials and log in"""

    return render_template('user_profile.html')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)