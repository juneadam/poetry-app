"""Create Read Update Delete operations."""

import model


# ============ users ============ #

def create_user(username, email, password, location=None):
    """Creates a User object to be added to the database."""

    user = model.User(username=username, email=email, password=password, location=location)

    return user


def find_user_by_email(email):
    """Check database for User object with matching email address."""

    return model.User.query.filter_by(email=email).first()

def find_user_by_id(user_id):
    """Check database for User object with matching user ID."""

    return model.User.query.filter_by(user_id=user_id).first()


# ============ bookmarks ============ #

def create_bookmark(title, author):
    """Creates a Poem object (a saved poem from the API)
    to be added to the database."""

    bookmark = model.Poem(title=title, author=author)

    return bookmark

def create_bookmark_lines(bk_poem_id, lines):
    """Saves the lines (in list form in the JSON) as rows
    on a table."""

    bookmark_lines = []

    for line in lines:
        bookmark_line = model.PoemLine(bk_poem_id=bk_poem_id, line=line)
        bookmark_lines.append(bookmark_line)
    
    return bookmark_lines


def find_bookmark_by_id(bk_poem_id):
    """Find bookmarked poem object using id number."""

    return model.Poem.query.filter_by(bk_poem_id=bk_poem_id).first()

def find_bookmark_by_title(title):
    """Find bookmarked poem object using title."""

    return model.Poem.query.filter_by(title=title).first()

def find_bookmark_by_author(author):
    """Generate a list of all poem objects using author name."""

    return model.Poem.query.filter_by(author=author).all()

def find_bookmark_all_lines_by_id(bk_poem_id):
    """Generate a list of all the lines of a poem, by id number."""

    return model.PoemLine.query.filter_by(bk_poem_id=bk_poem_id).all()


# ============ comments ============ #

def create_comment(user_id, bk_poem_id, user_notes=""):
    """Creates a Comment object to be added to the database."""

    comment = model.Comment(user_id=user_id, bk_poem_id=bk_poem_id, user_notes=user_notes)

    return comment

def find_all_comments_by_user_id(user_id):
    """Generates a list of all comment objects saved by a particular user."""

    return model.Comment.query.filter_by(user_id=user_id).all()

def find_comment_by_id(comment_id):
    """Finds a comment object using a particular id number."""

    return model.Comment.query.filter_by(comment_id=comment_id)


# ============ prompts ============ #

def create_prompt(prompt):
    """Creates a PromptDB object which can be added to the database."""

    return model.PromptDB(prompt_text=prompt)

def save_prompt_response(user_id, prompt_id, user_text):
    """Creates a SavedPrompt object which can be added to the database."""

    return model.SavedPrompt(user_id=user_id, prompt_id=prompt_id, user_text=user_text)


def get_all_prompts():
    """Generate a list of every prompt object in the database."""

    return model.PromptDB.query.all()

def find_prompt_by_text(prompt_text):
    """Look up a prompt by text of the prompt."""

    return model.PromptDB.query.filter(model.PromptDB.prompt_text==prompt_text).first()

def find_prompt_by_id(prompt_id):
    """Look up a prompt by id number."""

    return model.PromptDB.query.filter_by(prompt_id=prompt_id).first()

def find_all_saved_prompts_by_user_id(user_id):
    """Generate a list of every prompt saved by a particular user."""

    return model.SavedPrompt.query.filter_by(user_id=user_id).all()

def find_saved_prompt_by_saved_prompt_id(saved_prompt_id):
    """Look up a saved prompt by the saved prompt id number."""

    return model.SavedPrompt.query.filter_by(saved_prompt_id=saved_prompt_id).first()

def find_saved_prompts_by_id(prompt_id):
    """Generate a list of all saved prompts by database id number."""

    return model.SavedPrompt.query.filter_by(prompt_id=prompt_id).all()

def find_all_public_prompts():
    """Generate a list of all mashup objects from the database
    where the mashup_public attribute is set to True."""

    return model.SavedPrompt.query.filter_by(prompt_public=True).all()


# ============ mashups ============ #

def create_mashup(user_id, mashup_title, mashup_author):
    """Create a new mashup entry."""

    return model.Mashup(user_id=user_id, mashup_title=mashup_title, mashup_author=mashup_author)

def create_mashup_lines(mashup_id, lines):
    """Create a new mashup entry."""

    mashup_lines = []

    for line in lines:
        mashup_line = model.MashupLine(mashup_id=mashup_id, author_name=line[0], source_title=line[1], line=line[2])
        mashup_lines.append(mashup_line)

    return mashup_lines

def find_mashup_by_title(title):
    """Find a mashup in the database using it's title."""

    return model.Mashup.query.filter_by(mashup_title=title).first()

def find_mashup_by_id(mashup_id):
    """Find a mashup in the database using its id."""

    return model.Mashup.query.filter_by(mashup_id=mashup_id).first()

def find_mashup_lines_by_id(mashup_id):
    """Generate a list of all mashup lines by id."""

    return model.MashupLine.query.filter_by(mashup_id=mashup_id).all()

def find_all_mashups_by_user_id(user_id):
    """Generate a list of mashups from the database using user_id"""

    return model.Mashup.query.filter_by(user_id=user_id).all()

def find_all_public_mashups():
    """Generate a list of all mashup objects from the database
    where the mashup_public attribute is set to True."""

    return model.Mashup.query.filter_by(mashup_public=True).all()



if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    model.connect_to_db(app)
