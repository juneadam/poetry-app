"""Create Read Update Delete operations."""

import model

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

    return model.Poem.query.filter_by(bk_poem_id=bk_poem_id).first()

def find_bookmark_by_title(title):

    return model.Poem.query.filter_by(title=title).first()

def find_bookmark_by_author(author):

    return model.Poem.query.filter_by(author=author).first()


def create_comment(user_id, bk_poem_id, user_notes=""):
    """Creates a Comment object to be added to the database."""

    comment = model.Comment(user_id=user_id, bk_poem_id=bk_poem_id, user_notes=user_notes)

    return comment

def find_comment_by_id(comment_id):

    return model.Comment.query.filter_by(comment_id=comment_id)


def create_prompt(prompt):

    return model.PromptDB(prompt_text=prompt)

def get_all_prompts():

    return model.PromptDB.query.all()


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    model.connect_to_db(app)
