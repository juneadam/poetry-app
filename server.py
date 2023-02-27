"""server for poetry app"""
import os
from functools import wraps
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from passlib.hash import argon2
import pytest
from jinja2 import StrictUndefined
from random import choice, randint, shuffle
import requests
from model import connect_to_db, db
import crud
from utils import logged_in, logged_in_JSON, get_payload, form_easter_egg, range_modifier

dev = os.environ['dev']

app = Flask(__name__)
app.secret_key = dev
app.jinja_env.undefined = StrictUndefined


# ============ homepage/login/sign up routes ============ #

@app.route('/')
def show_homepage():
    """render the homepage"""

    return render_template('homepage.html',)

@app.route('/sign-up', methods=['POST'])
def user_sign_up():
    """allows the user to create a new account"""
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')    
    hashed_pw = argon2.hash(password1)
    user = crud.find_user_by_email(email=email)

    if user:
        flash("This email is already associated with an account. Please log in below.")
    else:
        if password1 != password2:
            flash("Passwords do not match, please try again.")
            return redirect('/')
        new_user = crud.create_user(email=email, username=username, password=hashed_pw)
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
        while True:
            if argon2.verify(password, user.password):
                if user.active_account == False:
                    return redirect('/reactivate-account-check')

                session['user_id'] = user.user_id
                session['username'] = user.username
                flash("You have logged in successfully!")
                return redirect('/')
            # else:
            session['user_id'] = None
            flash("Email and password do not match, please try again.")
            return redirect('/')
    else:
        session['user_id'] = None
        flash("User not found, please create an account below!")
        return redirect('/')

@app.route('/logout')
@logged_in
def logout():
    """Removes the user id from the session, logging them out."""

    session['user_id'] = None
    session['username'] = None
    flash('You have successfully logged out.')
    return redirect('/')


# ============ random poem routes ============ #

@app.route('/poems')
def show_poem_generator():
    """Render webpage which generates poems from PoetryDB API."""

    call_random_poem()

    return render_template('poems.html')

@app.route('/random-poem.json')
def call_random_poem():
    """Calls the API to get a random poem, sends to 
    the JS file to update poems.html"""

    res = requests.get('https://poetrydb.org/random')
    
    random_poem = res.json()

    return jsonify({'data': random_poem})

@app.route('/random-poem-with-inputs.json', methods=['POST'])
def call_random_poem_with_inputs():
    """Calls the API to get a random poem based on user inputs -
    including author, title, and line count - sends to the JS file 
    to update poems.html"""

    author = request.json.get('author-input')
    title = request.json.get('title-input')
    lines = request.json.get('lines-input')
    linecount = request.json.get('linecount-input')

    input_fields, output_fields = get_payload(author=author, title=title, lines=lines, linecount=linecount)

    url = f'https://poetrydb.org/{input_fields}/{output_fields}/all.json'

    res = requests.get(url)
    random_poem = []
    
    response_list = res.json()

    # PoetryDB API sends a dictionary {404: "not found"} if it returns no results - otherwise,
    # format is always a list of dictionaries [{}]
    if isinstance(response_list, dict):
        random_poem = [{'title': 'No Results Found', 'author': 'Please try other search parameters.', 'lines': ['Or just empty the inputs and click "New Poem".']}]
    else:
        if len(response_list) > 1:
            random_poem.append(response_list[randint(0, (len(response_list) - 1))])
        elif len(response_list) == 1:
            random_poem.append(response_list[0])

    return jsonify({'data': random_poem})


@app.route('/bookmark.json', methods=["POST"])
@logged_in_JSON
def bookmark_random_poem():
    """Saves comment and, if needed, poem to the database."""

    title = request.json.get('title')
    author = request.json.get('author')[2:]
    lines_string = request.json.get('lines')
    comments = request.json.get('comments')

    lines = lines_string.split('\n')
    bk_poem_id = ''
    bookmark_object = crud.find_bookmark_by_title(title)

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


# ============ prompts routes ============ #

@app.route('/prompts')
def show_prompt_generator():
    """Render webpage which generates poetry prompts from the toolkit database."""

    return render_template('prompts.html')


@app.route('/prompt-hole.json')
def call_random_prompt():
    """Display random writing prompt on screen."""

    prompts = crud.get_all_prompts()
    print(prompts)
    new_prompt = choice(prompts)

    return new_prompt.prompt_text

@app.route('/save-prompt.json', methods=['POST'])
@logged_in_JSON
def save_prompt_and_text():
    """Lets user bookmark a prompt and save their response to it."""

    prompt_text = request.json.get('prompt_text')
    user_response = request.json.get('user_response')

    promptDB_object = crud.find_prompt_by_text(prompt_text=prompt_text) 

    user_id = session['user_id']

    if promptDB_object:
        prompt_id = promptDB_object.prompt_id
        
        # get list of saved prompts by promptID
        prompt_list = crud.find_saved_prompts_by_id(prompt_id)

        # use a for loop to find the saved prompt that matches the user id
        for prompt in prompt_list:
            if prompt.user_id == user_id:
                prompt.user_text = user_response
                db.session.add(prompt)
                db.session.commit()
                return 'update'
            
        # if one is not found, create a new saved prompt object using
        #   user id, prompt id, and user response, then add and commit
        new_prompt_save = crud.save_prompt_response(user_id=user_id, prompt_id=prompt_id, user_text=user_response)
        db.session.add(new_prompt_save)
        db.session.commit()
        return 'fine'

    else:
        return 'error'


@app.route('/add-prompt')
@logged_in
def show_add_prompt_page():
    """Renders the page where users can add a new prompt to the database."""

    return render_template('add-prompt.html')

@app.route('/save-prompt-to-db.json', methods=['POST'])
@logged_in_JSON
def save_prompt_to_db():
    """Saves the new prompt to the database."""

    user_prompt = request.json.get('new_prompt')

    if user_prompt:
        new_prompt_obj = crud.create_prompt(prompt=user_prompt)

        db.session.add(new_prompt_obj)
        db.session.commit()
        return 'ok'

    return 'not ok'


# ============ load bookmarks routes ============#

@app.route('/savedpoem', methods=["POST"])
@logged_in
def load_bookmarked_poem_and_comments():
    """When clicking on a link, loads a page with title, author, and text
    of a particular poem, and loads the user's stored comments in the
    text box."""

    bk_poem_id = int(request.form.get('bk_poem_id'))
    user_id = session['user_id']
    username = session['username']

    poem_object = crud.find_bookmark_by_id(bk_poem_id=bk_poem_id)
    title = poem_object.title
    author = poem_object.author

    poem_lines_objs = crud.find_bookmark_all_lines_by_id(bk_poem_id=bk_poem_id)
    lines = []
    for line in poem_lines_objs:
        lines.append(line.line)

    comments = crud.find_all_comments_by_user_id(user_id)
    comment = ''
    for comment_obj in comments:
        if comment_obj.bk_poem_id == bk_poem_id:
            comment = comment_obj.user_notes

    return render_template("savedpoem.html",
                            title=title,
                            author=author,
                            lines=lines,
                            username=username,
                            user_text=comment)

@app.route('/savedprompt', methods=['POST'])
@logged_in
def load_bookmarked_prompt_and_response():
    """When clicking on a button, loads a page with the text of a 
    particular prompt, and loads the user's stored response in the
    text box."""

    user_id = session['user_id']
    username = session['username']

    saved_prompt_id = int(request.form.get('prompt_id'))
    prompt_id = ''

    prompt_response_list = crud.find_all_saved_prompts_by_user_id(user_id)
    user_response = ''
    for response in prompt_response_list:
        if int(response.saved_prompt_id) == saved_prompt_id:
            user_response = response.user_text
            prompt_id = response.prompt_id

    prompt_obj = crud.find_prompt_by_id(prompt_id)
    prompt_text = prompt_obj.prompt_text
    return render_template("savedprompt.html",
                            username=username,
                            prompt_text=prompt_text,
                            user_response=user_response)

@app.route('/savedmashup', methods=['POST'])
@logged_in
def load_saved_mashup():
    """When clicking on a button, loads a page with the
    text, title, and author of a user's saved mashup."""

    mashup_id = int(request.form.get('mashup_id'))
    mashup_obj = crud.find_mashup_by_id(mashup_id)
    mashup_title = mashup_obj.mashup_title
    username = mashup_obj.mashup_author

    mashup_lines_list = crud.find_mashup_lines_by_id(mashup_id)

    lines=[]
    for line in mashup_lines_list:
        lines.append({'line': line.line, 'author': line.author_name, 'source_title': line.source_title})

    return render_template('savedmashup.html',
                            username=username,
                            title=mashup_title,
                            lines=lines)


# ============ update bookmarks routes ============#

@app.route('/update-comments', methods=['POST'])
def update_saved_comments():
    """Overwrite the users's saved comments in the database
    with new edits."""

    user_id = session['user_id']
    updated_text = request.json.get('updated_text')
    title = request.json.get('title')

    poem_object = crud.find_bookmark_by_title(title)
    if not poem_object:
        return 'error'
    bk_poem_id = poem_object.bk_poem_id

    comments_by_user = crud.find_all_comments_by_user_id(user_id=user_id)
    comment_to_update = ''
    for comment_obj in comments_by_user:
        if comment_obj.bk_poem_id == bk_poem_id:
            comment_to_update = comment_obj  

    if comment_to_update:
        comment_to_update.user_notes = updated_text
        db.session.add(comment_to_update)
        db.session.commit()
        return "ok"
    
    elif not comment_to_update:
        return "error"


@app.route('/update-response', methods=['POST'])
def update_saved_response():
    """Overwrite the users's saved prompt response in the database
    with new edits."""
    
    user_id = session['user_id']

    updated_response = request.json.get('updated_response')
    prompt_text = request.json.get('prompt_text')

    prompt_id = crud.find_prompt_by_text(prompt_text).prompt_id
    response_obj_list = crud.find_saved_prompts_by_id(prompt_id)

    response_to_update = ''
    for response in response_obj_list:
        if response.user_id == user_id:
            response_to_update = response
            response_to_update.user_text = updated_response

    if response_to_update:
        db.session.add(response_to_update)
        db.session.commit()
        return 'ok'

    elif not response_to_update:
        return 'error'


# ============ mashup routes ============ #

@app.route('/mashups')
def show_mashup_generator():
    """Render webpage which generates poetry mashups from PoetryDB API."""

    return render_template('mashups.html')

@app.route('/mashup-generator.json', methods=['POST'])
def mashup_generator():
    """Call the API with user input linecount, generate a random
    poem mixing and matching lines from the returned list."""

    username = session.get('username')
    if username is None:
        username = 'Guest'

    linecount = int(request.json.get('linecount'))

    mashup_response = []
    for i in range(linecount, (linecount + range_modifier(linecount))):
        res = requests.get(f'https://poetrydb.org/linecount/{i}/all.json')
        mashup_response.extend(res.json())

    title_list = []
    for i in range(0, 4):
        poem = choice(mashup_response)
        title_choice = poem['title'].split()
        for word in title_choice:
            title_list.append(word)
    
    shuffle(title_list)

    title = f'{title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'
    linecount_prefix = form_easter_egg(linecount)
    if linecount_prefix:
        title = linecount_prefix + title

    poems_by_line_tuples_list = []

    for i in range(0, linecount):
        poem = choice(mashup_response)
        while poem['lines'][i] == '':
            poem = choice(mashup_response)
        poems_by_line_tuples_list.append((poem['author'], poem['title'], poem['lines'][i]))
    
    return jsonify({'data': poems_by_line_tuples_list, 
                    'username': username,
                    'title': title})

@app.route('/save-mashup.json', methods=['POST'])
@logged_in_JSON
def save_mashup():
    """Route to save a mashup to the database."""

    user_id = session['user_id']
    dataList = request.json.get('dataList')
    title = request.json.get('title')
    author = request.json.get('author')[3:-13]

    if dataList == []:
        return 'empty'

    mashup_obj = crud.find_mashup_by_title(title)

    # if mashup_obj:
    #     print(f'\n\n\nmashup_lines {mashup_obj.lines}\n\n')
    #     print(f'\n\n dataList {dataList}\n\n')
    
    new_mashup = crud.create_mashup(user_id=user_id, mashup_title=title, mashup_author=author)
    db.session.add(new_mashup)
    db.session.commit()

    mashup_obj = crud.find_mashup_by_title(title)
    mashup_id = mashup_obj.mashup_id

    mashup_lines = []
    for line in dataList:
        split_line = line.split('@')
        mashup_lines.append(split_line)

    new_mashup_lines = crud.create_mashup_lines(mashup_id=mashup_id, lines=mashup_lines)

    db.session.add_all(new_mashup_lines)
    db.session.commit()

    return 'ok'


# ============ user profile routes ============ #

@app.route('/userprofile')
@logged_in
def user_profile_with_react():
    """User profile with React"""

    return render_template('userprofile.html')


@app.route('/username.json')
def fetch_username_json():
    """Fetch username from the database."""

    username = session['username']
    
    return username

@app.route('/username-corner.json')
def fetch_username_corner_json():
    """Fetch username from the database."""

    if session.get('username'):
        username = session['username']
    else:
        username = 'Account'
    
    return username


@app.route('/user-saved-bookmarks.json')
def fetch_bookmarks_json():
    """Fetch user bookmarks from the database."""
    user_id = session['user_id']

    user_comments = crud.find_all_comments_by_user_id(user_id)
    bk_poem_ids = []
    for comment in user_comments:
        if comment.bk_poem_id not in bk_poem_ids:
            bk_poem_ids.append(comment.bk_poem_id)

    bookmarks = []
    for bkid in bk_poem_ids:
        poem = crud.find_bookmark_by_id(bkid)
        poem_id = poem.bk_poem_id
        title = poem.title
        author = poem.author
        bookmarks.append((poem_id, title, author))

    return jsonify({'bookmarks': bookmarks})

@app.route('/user-saved-prompts.json')
def fetch_prompts_json():
    """user prompts"""
    user_id = session['user_id']

    user_prompts = crud.find_all_saved_prompts_by_user_id(user_id)
    prompt_texts = []
    for saved_prompt in user_prompts:
        prompt_in_db = crud.find_prompt_by_id(saved_prompt.prompt_id)
        prompt_texts.append((saved_prompt.saved_prompt_id, saved_prompt.user_text, prompt_in_db.prompt_text, saved_prompt.prompt_public))

    return jsonify({'user_prompts': prompt_texts})

@app.route('/user-saved-mashups.json')
def fetch_mashups_json():
    """Fetch user mashups from the database."""
    user_id = session['user_id']
    user_mashups = crud.find_all_mashups_by_user_id(user_id)

    mashups = []
    for mashup in user_mashups:
        mashups.append((mashup.mashup_id, mashup.mashup_title, mashup.mashup_public))

    return jsonify({'user_mashups': mashups})

    
# ============ public / private toggle routes ============#

@app.route('/update-prompt-bool.json', methods=["POST"])
def update_prompt_bool_in_db():
    """Allows the user to change the boolean in the database that controls
    whether a prompt and response they've saved are publicly visible."""

    user_id = session['user_id']
    public_check = bool(request.json.get('public_check'))
    saved_prompt_id = int(request.json.get('saved_prompt_id'))

    saved_prompt = crud.find_saved_prompt_by_saved_prompt_id(saved_prompt_id=saved_prompt_id)
    
    if saved_prompt.user_id != user_id:
        return 'wrong user'
    
    saved_prompt.prompt_public = public_check
    db.session.add(saved_prompt)
    db.session.commit()

    return 'ok'

@app.route('/update-mashup-bool.json', methods=["POST"])
def update_mashup_bool_in_db():
    """Allows the user to change the boolean in the database that controls
    whether a mashup they've saved is publicly visible."""

    user_id = session.get('user_id')
    public_check = bool(request.json.get('public_check'))
    saved_mashup_id = int(request.json.get('saved_mashup_id'))


    saved_mashup = crud.find_mashup_by_id(mashup_id=saved_mashup_id)
    
    if saved_mashup.user_id != user_id:
        return 'wrong user'
    
    saved_mashup.mashup_public = public_check
    db.session.add(saved_mashup)
    db.session.commit()

    return 'ok'


# ============ deactivate/reactivate account routes ============ #

@app.route('/deactivate-account-check', methods=["GET", "POST"])
def render_deactivate_page():
    """Renders the page where users can enter their password to deactivate their account."""

    return render_template("/deactivate-splash.html")

@app.route('/deactivate-account', methods=["POST"])
def deactivate_account():
    """Logic for deactivating a user's account."""

    email = request.form.get('user-email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user_id = session['user_id']

    user = crud.find_user_by_email(email=email)

    if password1 != password2:
        flash("Passwords do not match, please try again.")
        return redirect('/deactivate-account-check')

    if not user or user.user_id != user_id:
        flash("Please make sure you are logged in to the correct account.")
        return redirect('/deactivate-account-check')

    if not argon2.verify(password1, user.password):
        flash("Account credentials incorrect.")
        return redirect('/deactivate-account-check')

    if argon2.verify(password1, user.password):
        user.active_account = False
        db.session.add(user)
        db.session.commit()

        user_mashups = crud.find_all_mashups_by_user_id(user_id)
        for mashup in user_mashups:
            mashup.mashup_public = False
        db.session.add_all(user_mashups)
        db.session.commit()

        user_prompts = crud.find_all_saved_prompts_by_user_id(user_id)
        for prompt in user_prompts:
            prompt.prompt_public = False
        db.session.add_all(user_prompts)
        db.session.commit()

    flash("Account successfully deactivated.")
    return redirect('/')

@app.route('/reactivate-account-check')
def render_reactivate_page():
    """Splash page to let user reactivate their account if they wish."""

    return render_template("/reactivate-account.html")

@app.route('/reactivate-account', methods=["POST"])
def reactivate_account():
    """Logic for reactivating a user's account."""
    
    email = request.form.get('user-email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user_id = session['user_id']

    user = crud.find_user_by_email(email=email)

    if password1 != password2:
        flash("Passwords do not match, please try again.")
        return redirect('/reactivate-account-check')

    if not user or user.user_id != user_id:
        flash("Please make sure you are logged in to the correct account.")
        return redirect('/reactivate-account-check')

    if not argon2.verify(password1, user.password):
        flash("Account credentials incorrect.")
        return redirect('/reactivate-account-check')

    if argon2.verify(password1, user.password):
        user.active_account = True
        db.session.add(user)
        db.session.commit()

    flash("Account successfully reactivated! We're glad to have you back :)")
    return redirect('/userprofile')


# ============ public lists routes ============ #

@app.route('/search-responses')
@logged_in
def show_prompts_list():
    """Render the page that displays public user prompt responses."""

    return render_template('publicprompts.html')

@app.route('/public-prompts.json')
def fetch_public_prompts():
    """Generate a list of public prompt objects using crud function."""

    prompts_list = crud.find_all_public_prompts()

    prompts_data = []
    for prompt in prompts_list:
        prompt_text = crud.find_prompt_by_id(prompt.prompt_id).prompt_text
        author_username = crud.find_user_by_id(prompt.user_id).username
        
        prompts_data.append((prompt.saved_prompt_id, prompt_text, author_username, prompt.user_text))

    shuffle(prompts_data)

    return jsonify({'responses': prompts_data})

@app.route('/search-mashups')
@logged_in
def show_mashups_list():
    """Render the page that displays public user mashups."""

    return render_template('publicmashups.html')

@app.route('/public-mashups.json')
def fetch_public_mashups():
    """Generate a list of public prompt objects using crud function."""

    mashups_list = crud.find_all_public_mashups()
    mashups_data = []
    for mashup in mashups_list:
        mashups_data.append((mashup.mashup_id, mashup.mashup_title, mashup.mashup_author))

    shuffle(mashups_data)

    return jsonify({'mashups': mashups_data})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=False)
    import sys
    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True