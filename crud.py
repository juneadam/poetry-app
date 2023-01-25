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


def create_bookmark(api_url, title, author, full_text):
    """Creates a LibraryDB object (a saved poem from the API)
    to be added to the database."""

    bookmark = model.Poem(api_url=api_url, title=title, author=author, full_text=full_text)

    return bookmark

def find_bookmark_by_id(bk_poem_id):

    return model.Poem.query.filter_by(bk_poem_id=bk_poem_id)


def create_comment(user_id, bk_poem_id, user_notes=""):
    """Creates a Comment object to be added to the database."""

    comment = model.Comment(user_id=user_id, bk_poem_id=bk_poem_id, user_notes=user_notes)

    return comment

def find_comment_by_id(comment_id):

    return model.Comment.query.filter_by(comment_id=comment_id)


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    model.connect_to_db(app)
