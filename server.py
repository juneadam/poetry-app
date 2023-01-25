"""server for poetry app"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db

from crud import create_user, find_user_by_email

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """render the homepage"""

    return render_template('homepage.html')

@app.route('/sign-up', methods=['POST'])
def user_sign_up():
    """allows the user to create a new account"""
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = find_user_by_email(email=email)

    if user:
        flash("This email is already associated with an account. Please log in below.")
    else:
        new_user = create_user(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account was created successfully! You may now login.')
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def user_login():
    """check user credentials and log in"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = find_user_by_email(email=email)

    if user:
        if user.password == password:
            session['user_id'] = user.user_id
            flash("You have logged in successfully!")
            return redirect('/')
        else:
            session['user_id'] = None
            flash("Email and password do not match, please try again.")
            return redirect('/')
    else:
        flash("User not found, please create an account below!")
        return redirect('/')

@app.route('/poems')
def show_poem_generator():
    """Render webpage which generates poems from PoetryDB API."""

    return render_template('poems.html')

@app.route('/prompts')
def show_prompt_generator():
    """Render webpage which generates poetry prompts from the toolkit database."""

    return render_template('prompts.html')

@app.route('/mashups')
def show_mashup_generator():
    """Render webpage which generates poetry mashups from PoetryDB API."""

@app.route('/userpage')
def user_profile():
    """Render user profile."""

    return render_template('userpage.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)