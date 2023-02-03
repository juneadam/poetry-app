"""server for poetry app"""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)

import requests

from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

from random import choice, randint, shuffle

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# ------------ homepage/login/sign up routes ------------ #

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

@app.route('/logout')
def logout():
    """Removes the user id from the session, logging them out."""

    session['user_id'] = None
    print(session['user_id'])
    flash('You have successfully logged out.')
    return redirect('/')



# ------------ random poem routes ------------ #

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

    payload = []

    if author:
        payload.append(('author', author))
    if title:
        payload.append(('title', title))
    if lines:
        payload.append(('lines', lines))
    if linecount:
        payload.append(('linecount', linecount))

    input_fields = ''
    output_fields = ''

    for tup in payload:
        input_fields = input_fields + tup[0] + ',' #/author,title,linecount/shakespeare;sonnet;14
        output_fields = output_fields + tup[1] + ';'

    input_fields = input_fields[:-1]
    output_fields = output_fields[:-1]

    url = f'https://poetrydb.org/{input_fields}/{output_fields}/all.json'
    print(f'\n\n url {url}\n\n')

    res = requests.get(url)
    random_poem = []
    
    response_list = res.json()
    print(response_list)

    if isinstance(response_list, dict):
        random_poem = [{'title': 'No Results Found', 'author': 'Please try other search parameters.', 'lines': ['Or just empty the inputs and click "New Poem".']}]
    else:
        if len(response_list) > 1:
            random_poem.append(response_list[randint(0, (len(response_list) - 1))])
        elif len(response_list) == 1:
            random_poem.append(response_list[0])

    print(random_poem)

    print(f"\n random_poem: {random_poem}\n\n")

    return jsonify({'data': random_poem})


@app.route('/bookmark', methods=["POST"])
def bookmark_random_poem():
    """Saves comment and, if needed, poem to the database."""

    title = request.json.get('title')
    author = request.json.get('author')[2:]
    lines_string = request.json.get('lines')
    comments = request.json.get('comments')

    print(author)

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
    """Display random writing prompt on screen."""

    prompts = crud.get_all_prompts()

    new_prompt = choice(prompts)

    return new_prompt.prompt_text


@app.route('/save-prompt', methods=['POST'])
def save_prompt_and_text():
    """Lets user bookmark a prompt and save their response to it."""

    prompt_text = request.json.get('prompt_text')
    user_response = request.json.get('user_response')
    # print(f'\n\n\n\n prompt_text: {prompt_text} \n\n\n')
    # print(f'\n\n\n\n user_response: {user_response} \n\n\n')

    promptDB_object = crud.find_prompt_by_text(prompt_text=prompt_text)

    # print(f'\n\n\n\n promptDB_object: {promptDB_object} \n\n\n')
    
    if not session.get('user_id'):

        return 'nope'

    else:
        user_id = session['user_id']

        if promptDB_object:
            prompt_id = promptDB_object.prompt_id
            
            # get list of saved prompts by promptID
            prompt_list = crud.find_saved_prompts_by_id(prompt_id)

            # use a for loop to find the saved prompt that matches the user id
            for prompt in prompt_list:
                if prompt.user_id == user_id:
                # if one is found, use crud function (NEED TO CREATE) to update
                #   the text of that saved prompt
                    return 'update'
             
            # if one is not found, create a new saved prompt object using
            #   user id, prompt id, and user response, then add and commit
            new_prompt_save = crud.save_prompt_response(user_id=user_id, prompt_id=prompt_id, user_text=user_response)
            db.session.add(new_prompt_save)
            db.session.commit()

            return 'fine'

        else:

            return 'error'


# ------------ load bookmarks routes ------------#

@app.route('/savedpoem', methods=["POST"])
def load_bookmarked_poem_and_comments():
    """When clicking on a link, loads a page with title, author, and text
    of a particular poem, and loads the user's stored comments in the
    text box."""

    bk_poem_id = int(request.form.get('bk_poem_id'))
    user_id = session['user_id']

    # print(f'\n\n\n{type(bk_poem_id)}\n\n\n')

    poem_object = crud.find_bookmark_by_id(bk_poem_id=bk_poem_id)
    title = poem_object.title
    author = poem_object.author

    poem_lines_objs = crud.find_bookmark_all_lines_by_id(bk_poem_id=bk_poem_id)
    lines = []
    for line in poem_lines_objs:
        lines.append(line.line)

    user_obj = crud.find_user_by_id(user_id)
    username = user_obj.username

    comments = crud.find_all_comments_by_user_id(user_id)
    comment = ''
    print(f'\n\n\n comments: {comments}')
    for comment_obj in comments:
        if comment_obj.bk_poem_id == bk_poem_id:
            comment = comment_obj.user_notes
            print(f'\n\n\n user_notes: {comment_obj.user_notes}')

    # print(f"\n\n comment: {comment} \n\n")
    # print(f"\n\n poem_object: {poem_object} \n\n")
    # print(f"\n\n bk_poem_id: {bk_poem_id} \n\n")
    # print(f"\n\n user_id: {user_id} \n\n")
    # print(f"\n\n {lines} \n\n")

    return render_template("savedpoem.html",
                            title=title,
                            author=author,
                            lines=lines,
                            username=username,
                            user_text=comment)


@app.route('/savedprompt', methods=['POST'])
def load_bookmarked_prompt_and_response():
    """When clicking on a link, loads a page with the text of a 
    particular prompt, and loads the user's stored response in the
    text box."""

    user_id = session['user_id']
    user_obj = crud.find_user_by_id(user_id=user_id)
    username = user_obj.username

    prompt_id = int(request.form.get('prompt_id'))
    prompt_obj = crud.find_prompt_by_id(prompt_id)
    prompt_text = prompt_obj.prompt_text

    prompt_response_list = crud.find_all_saved_prompts_by_user_id(user_id)
    user_response = ''
    for response in prompt_response_list:
        if response.prompt_id == prompt_id:
            user_response = response.user_text
            # print(f'\n\n\n response {response} \n\n\n')

    # print(f'\n\n\n prompt_response_list {prompt_response_list}')
    # print(f'\n\n\n prompt_id {prompt_id}')
    # print(f'\n\n\n user_id {user_id}')
    # print(f'\n\n\n prompt_text {prompt_text}')
    # print(f'\n\n\n user_response {user_response}')

    return render_template("savedprompt.html",
                            username=username,
                            prompt_text=prompt_text,
                            user_response=user_response)

@app.route('/savedmashup', methods=['POST'])
def load_saved_mashup():
    """When clicking on a button, loads a page with the
    text, title, and author of a user's saved mashup."""

    pass


# ------------ update bookmarks routes ------------#

@app.route('/update-comments', methods=['POST'])
def update_saved_comments():
    """Overwrite the users's saved comments in the database
    with new edits."""

    user_id = session['user_id']
    # print(f'\n\n\nuser_id type: {type(user_id)}\n\n')
    updated_text = request.json.get('updated_text')
    title = request.json.get('title')
    # author = request.json.get('author')
    # print(f'\n\n\ntitle: {title} author: {author}\nnew_text: {updated_text}\n\n')

    poem_object = crud.find_bookmark_by_title(title)
    bk_poem_id = poem_object.bk_poem_id
    # print(f'\n\n\nbk_poem_id: {bk_poem_id}\n\n\n')

    comments_by_user = crud.find_all_comments_by_user_id(user_id=user_id)
    comment_to_update = ''
    for comment_obj in comments_by_user:
        if comment_obj.bk_poem_id == bk_poem_id:
            comment_to_update = comment_obj
    
    # print(f'\n\n\ncomment_to_update: {comment_to_update.user_notes}\n\n\n')

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
    # print(f'\n\n\nuser_id type: {type(user_id)}\n\n')

    updated_response = request.json.get('updated_response')
    prompt_text = request.json.get('prompt_text')

    # print(f'\n\n\nupdated_response: {updated_response}')
    # print(f'\n\n\nprompt_text: {prompt_text}')

    prompt_id = crud.find_prompt_by_text(prompt_text).prompt_id
    response_obj_list = crud.find_saved_prompts_by_id(prompt_id)
    # print(f'\n\n\nresponse_obj_list: {response_obj_list}')

    response_to_update = ''
    for response in response_obj_list:
        if response.user_id == user_id:
            response_to_update = response
            # print(f'\n\n\nresponse_to_update: {response_to_update.user_text}')
            response_to_update.user_text = updated_response

    if response_to_update:
        db.session.add(response_to_update)
        db.session.commit()
        return 'ok'

    elif not response_to_update:
        return 'error'


# ------------ mashup routes ------------ #

@app.route('/mashups')
def show_mashup_generator():
    """Render webpage which generates poetry mashups from PoetryDB API."""

    return render_template('mashups.html')

@app.route('/mashup-generator', methods=['POST'])
def mashup_generator():
    """Call the API with user input linecount, generate a random
    poem mixing and matching lines from the returned list."""

    user_id = session['user_id']
    username = crud.find_user_by_id(user_id).username

    linecount = int(request.json.get('linecount'))

    res = requests.get(f'https://poetrydb.org/linecount/{linecount}/all.json')
    mashup_response = res.json()

    print(f'\n\nmashup_response {mashup_response}\n\n')

    title_list = []
    for i in range(0, 2):
        poem = choice(mashup_response)
        title_choice = poem['title'].split()
        for word in title_choice:
            title_list.append(word)
    
    shuffle(title_list)

    title = ''
    if linecount !=3 and linecount != 5 and linecount != 14 and linecount !=19 and linecount !=100:
        title = f'{title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'
    elif linecount == 3:
        title = f'Haiku: {title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'
    elif linecount == 5:
        title = f'Limerick: {title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'
    elif linecount == 14:
        title = f'Sonnet: {title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'
    elif linecount == 19:
        title = f'Villanelle: {title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'    
    elif linecount == 100:
        title = f'Cento: {title_list[0]} {title_list[1]} {title_list[2]} {title_list[3]}'

    # print(title)

    poems_by_line_tuples_list = []

    for i in range(0, linecount):
        poem = choice(mashup_response)
        poems_by_line_tuples_list.append((poem['author'], poem['title'], poem['lines'][i]))

    # print(f'\n\n\npoems_list: {poems_by_line_tuples_list}\n\n')
    
    return jsonify({'data': poems_by_line_tuples_list, 
                    'username': username,
                    'title': title})

@app.route('/save-mashup', methods=['POST'])
def save_mashup():
    """Route to save a mashup to the database."""

    user_id = session['user_id']
    dataList = request.json.get('dataList')
    title = request.json.get('title')
    author = request.json.get('author')[3:-13]

    # print(f'\n\n\ndataList {dataList}\n')
    # print(f'\n\ntitle {title}\n')
    # print(f'\n\nauthor {author} {len(author)}\n')

    if not user_id:
        return 'not ok'

    else:
        
        new_mashup = crud.create_mashup(user_id=user_id, mashup_title=title, mashup_author=author)
        db.session.add(new_mashup)
        db.session.commit()

        mashup_obj = crud.find_mashup_by_title(title)
        mashup_id = mashup_obj.mashup_id
        print(f'\n\n\n{mashup_id}\n\n\n')

        mashup_lines = []
        for line in dataList:
            split_line = line.split('@')
            mashup_lines.append(split_line)

        print(mashup_lines)

        new_mashup_lines = crud.create_mashup_lines(mashup_id=mashup_id, lines=mashup_lines)
        print(new_mashup_lines)

        db.session.add_all(new_mashup_lines)
        db.session.commit()

        return 'ok'


# ------------ user profile routes ------------ #

@app.route('/userprofile')
def user_profile():
    """Render user profile. This route is built without
    React and will be deprecated."""

    logged_in = session.get('user_id')
    print(logged_in)

    if not logged_in:
        flash('You are not logged in. Please log in below:')
        return redirect('/')
    else:
        user = crud.find_user_by_id(logged_in)
        username = user.username

        user_comments = crud.find_all_comments_by_user_id(logged_in)
        bk_poem_ids = []
        for comment in user_comments:
            if comment.bk_poem_id not in bk_poem_ids:
                bk_poem_ids.append(comment.bk_poem_id)
        
        # print(f'\n\n\n\n\n bk_poem_ids {bk_poem_ids} \n\n\n\n')
        

        bookmarks = []
        for bkid in bk_poem_ids:
            poem = crud.find_bookmark_by_id(bkid)
            poem_id = poem.bk_poem_id
            title = poem.title
            author = poem.author
            bookmarks.append((poem_id, title, author))

        # print(f'\n\n\n\n\n bookmarks {bookmarks} \n\n\n\n')
        
        
        user_prompts = crud.find_all_saved_prompts_by_user_id(logged_in)
        prompt_texts = []
        for saved_prompt in user_prompts:
            prompt_in_db = crud.find_prompt_by_id(saved_prompt.prompt_id)
            prompt_texts.append((saved_prompt.prompt_id, saved_prompt.user_text, prompt_in_db.prompt_text))

        # print(f'\n\n\n\n\n prompt_texts {prompt_texts} \n\n\n\n')        
        
        
        return render_template('userprofile.html',
                                username=username,
                                bookmarks=bookmarks,
                                prompt_texts=prompt_texts)


@app.route('/userprofiletest')
def user_profile_with_react():
    """user profile"""

    return render_template('userprofiletest.html')


@app.route('/username.json')
def fetch_username_json():
    """username"""

    user_id = session['user_id']

    user = crud.find_user_by_id(user_id)
    username = user.username

    return username

@app.route('/user-saved-bookmarks.json')
def fetch_bookmarks_json():
    """user bookmarks"""
    
    user_id = session['user_id']

    user_comments = crud.find_all_comments_by_user_id(user_id)
    bk_poem_ids = []
    for comment in user_comments:
        if comment.bk_poem_id not in bk_poem_ids:
            bk_poem_ids.append(comment.bk_poem_id)

    # print(f'\n\n\n\n\n bk_poem_ids {bk_poem_ids} \n\n\n\n')

    bookmarks = []
    for bkid in bk_poem_ids:
        poem = crud.find_bookmark_by_id(bkid)
        poem_id = poem.bk_poem_id
        title = poem.title
        author = poem.author
        bookmarks.append((poem_id, title, author))
    
    # print(f'\n\n\n\n\n bookmarks {bookmarks} \n\n\n\n')

    return jsonify({'bookmarks': bookmarks})

@app.route('/user-saved-prompts.json')
def fetch_prompts_json():
    """user prompts"""

    user_id = session['user_id']

    user_prompts = crud.find_all_saved_prompts_by_user_id(user_id)
    prompt_texts = []
    for saved_prompt in user_prompts:
        prompt_in_db = crud.find_prompt_by_id(saved_prompt.prompt_id)
        prompt_texts.append((saved_prompt.prompt_id, saved_prompt.user_text, prompt_in_db.prompt_text))

    # print(f'\n\n\nuser_prompts: {prompt_texts}\n\n\n')

    return jsonify({'user_prompts': prompt_texts})

@app.route('/user-saved-mashups.json')
def fetch_mashups_json():
    """user mashups"""

    user_id = session['user_id']

    user_mashups = crud.find_all_mashups_by_user_id(user_id)

    mashups = []
    for mashup in user_mashups:
        mashups.append((mashup.mashup_id, mashup.mashup_title))

    return jsonify({'user_mashups': mashups})





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)