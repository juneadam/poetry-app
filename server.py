"""server for poetry app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)

import requests

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

from random import choice

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# ------------ home page/login/sign up routes ------------ #

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
    user = crud.find_user_by_email(email=email)

    if user:
        flash("This email is already associated with an account. Please log in below.")
    else:
        new_user = crud.create_user(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account was created successfully! You may now login.')
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def user_login():
    """check user credentials and log in"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.find_user_by_email(email=email)

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

# ------------ random poem routes ------------ #

@app.route('/poems')
def show_poem_generator():
    """Render webpage which generates poems from PoetryDB API."""

    call_random_poem()

    return render_template('poems.html')

@app.route('/random-poem')
def call_random_poem():
    """Calls the API to get a random poem, sends to the JS file to update poems.html, 
    adds poem data to the session in case poem is bookmarked (deprecated)."""

    res = requests.get('https://poetrydb.org/random')
    
    random_poem = res.json()

    # session['random_poem'] = {}

    # session['random_poem']['title'] = random_poem[0]['title']
    # session['random_poem']['author'] = random_poem[0]['author']
    # session['random_poem']['lines'] = random_poem[0]['lines']

    # print(f"session title is: {session['random_poem']['title']}")
    # print(f"session title is: {session['random_poem']['author']}")
    # print(f"session title is: {session['random_poem']['lines']}")

    return jsonify({'data': random_poem})


@app.route('/bookmark', methods=["POST"])
def bookmark_random_poem():
    """Saves comment and, if needed, poem to the database."""

    title = request.json.get('title')
    author = request.json.get('author')
    lines_string = request.json.get('lines')
    comments = request.json.get('comments')

    lines = lines_string.split('\n')
    
    bk_poem_id = ''

    bookmark_object = crud.find_bookmark_by_title(title)

    if not session.get('user_id'):

        return 'not ok'

    else:

        user_id = session['user_id']

        if bookmark_object:
            if bookmark_object.author == author:
                bk_poem_id = bookmark_object.bk_poem_id
        
        else:
            new_bookmark = crud.create_bookmark(title=title, author=author)
            db.session.add(new_bookmark)
            db.session.commit()
            
            bookmark_object = crud.find_bookmark_by_title(title)
            bk_poem_id = bookmark_object.bk_poem_id

            new_lines = crud.create_bookmark_lines(bk_poem_id=bk_poem_id, lines=lines)
            db.session.add_all(new_lines)
            db.session.commit()

        new_comment = crud.create_comment(user_id=user_id, bk_poem_id=bk_poem_id, user_notes=comments)    
        db.session.add(new_comment)
        db.session.commit()

        return 'ok'


# ------------ prompts routes ------------ #

@app.route('/prompts')
def show_prompt_generator():
    """Render webpage which generates poetry prompts from the toolkit database."""

    return render_template('prompts.html')


@app.route('/prompt-hole')
def call_random_prompt():
    """Display random poetry prompt on screen."""

    prompts = crud.get_all_prompts()

    new_prompt = choice(prompts)

    return jsonify(new_prompt.prompt_text)




# ------------ mashups routes ------------ #

@app.route('/mashups')
def show_mashup_generator():
    """Render webpage which generates poetry mashups from PoetryDB API."""

    return render_template('mashups.html')


# ------------ user profile routes ------------ #

@app.route('/userprofile')
def user_profile():
    """Render user profile."""

    logged_in = session.get('user_id')
    print(logged_in)

    if session.get('user_id') is None:
        flash('You are not logged in. Please log in below:')
        return redirect('/')
    else:
        return render_template('userprofile.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)