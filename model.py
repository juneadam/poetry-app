"""Models for poetry tools app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ------------ User Data ------------ #

class User(db.Model):
    """Creates a table to save user data."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(99), unique=True)
    active_account = db.Column(db.Boolean, default=True, nullable=False)
    location = db.Column(db.String(255), nullable=True)

    comments = db.relationship("Comment", back_populates="user")
    mashups = db.relationship("Mashup", back_populates="user")
    saved_prompts = db.relationship("SavedPrompt", back_populates="user")
    saved_linebreaks = db.relationship("SavedLinebreak", back_populates="user")

    def __repr__(self):
        return f'<User object user_id: {self.user_id} username: {self.username}>'


# ------------ Poem Comments/Bookmarks ------------ #

class Comment(db.Model):
    """Creates a table to track user comments associated with
    bookmarked poems."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    user_notes = db.Column(db.Text)
    bk_poem_id = db.Column(db.Integer, 
                        db.ForeignKey('poems.bk_poem_id'))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))

    user = db.relationship("User", back_populates="comments")
    saved_poem = db.relationship("Poem", back_populates="comments")


    def __repr__(self):
        return f'<Comment object bk_poem_id: {self.bk_poem_id} user_id: {self.user_id}>'

class Poem(db.Model):
    """Creates a table for saving API-generated poems that 
    users wish to bookmark for future reading."""

    __tablename__ = "poems"

    bk_poem_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(150))

    comments = db.relationship("Comment", back_populates="saved_poem")
    lines = db.relationship("PoemLine", back_populates="saved_poem")

    def __repr__(self):
        return f'<Poem object bk_poem_id: {self.bk_poem_id} title: {self.title} author: {self.author}>'


class PoemLine(db.Model):

    __tablename__ = "poemlines"

    bk_line_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    bk_poem_id = db.Column(db.Integer, 
                        db.ForeignKey("poems.bk_poem_id"),
                        nullable=False)
    line = db.Column(db.Text)

    saved_poem = db.relationship("Poem", back_populates="lines")

    def __repr__(self):
        return f'<PoemLine object bk_poem_id: {self.bk_poem_id} bk_line_id: {self.bk_line_id}>'


# ------------ Mashup ------------ #

class Mashup(db.Model):
    """Creates a table for API-generated mashup poems
    that the user wants to save."""

    __tablename__ = "mashups"

    mashup_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    mashup_title = db.Column(db.Text)
    mashup_author = db.Column(db.Text)
    mashup_public = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("User", back_populates="mashups")
    lines = db.relationship("MashupLine", back_populates="mashup")

    def __repr__(self):
        return f'<Mashup object mashup_id: {self.mashup_id} user_id: {self.user_id}>'


class MashupLine(db.Model):
    """Creates a table for components making up particular 
    mashup poems saved by the user."""

    __tablename__ = "mashuplines"

    component_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    mashup_id = db.Column(db.Integer,
                        db.ForeignKey("mashups.mashup_id"))
    author_name = db.Column(db.String(255))
    source_title = db.Column(db.String(255))
    line = db.Column(db.Text)

    mashup = db.relationship("Mashup", back_populates="lines")

    def __repr__(self):
        return f'<MashupLine object mashup_line_id: {self.component_id} author_name: {self.author_name} source_title: {self.source_title} line: {self.line}>'


# ------------ Prompts ------------ #

class PromptDB(db.Model):
    """Database of poetry prompts to choose from."""

    __tablename__ = "prompts"

    prompt_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    prompt_text = db.Column(db.String(255), unique=True)

    saved_prompts = db.relationship("SavedPrompt", back_populates="prompt")

    def __repr__(self):
        return f'<PromptDB object prompt_id: {self.prompt_id}>'


class SavedPrompt(db.Model):
    """Table allowing a user to bookmark a prompt they particularly like."""

    __tablename__ = "savedprompts"

    saved_prompt_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    prompt_id = db.Column(db.Integer,
                        db.ForeignKey("prompts.prompt_id"))
    user_text = db.Column(db.Text)
    prompt_public = db.Column(db.Boolean, default=False, nullable=False)

    prompt = db.relationship("PromptDB", back_populates="saved_prompts")
    user = db.relationship("User", back_populates="saved_prompts")

    def __repr__(self):
        return f'<SavedPrompt object saved_prompt_id: {self.saved_prompt_id} user_id: {self.user_id} prompt_id: {self.prompt_id}>'


# ------------ Line Breaks ------------#

class SavedLinebreak(db.Model):
    """Table allowing user to save their poems with randomly generated
    line-breaks."""

    __tablename__ = "saveduserpoems"

    linebreak_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    poem = db.Column(db.Text)
    public = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="saved_linebreaks")

    def __repr__(self):
        return f'<UserLinebreak object linebreak_id: {self.linebreak_id} user_id: {self.user_id} public: {self.public}'


# ------------ Etc. ------------ #

def connect_to_db(flask_app, db_uri="postgresql:///poetrytoolkitDB", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()