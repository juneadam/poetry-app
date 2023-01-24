"""Models for poetry tools app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def User(db.Model):
    """Creates a table to save user data."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password - db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(99), unique=True)
    active_account = db.Column(db.Boolean, default=True, nullable=False)
    location = db.Column(db.String(255), nullable=True)

    comments = db.relationship("Comment", back_populates="user")
    mashups = db.relationship("Mashup", back_populates="user")
    saved_prompts = db.relationship("SavedPrompt", back_populates="user")

    saved_linebreaks = db.relationship("SavedLinebreak", back_populates="user")

    def __repr__(self):
        return f'<User object user_id: {self.user_id} username: {self.username}>'


def Comment(db.Model):
    """Creates a table to track user comments associated with
    bookmarked poems."""

    __tablename__ = 'poem_notes'

    poem_notes_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    user_notes = db.Column(db.Text)
    bk_poem_id = db.Column(db.Integer, 
                        db.ForeignKey('saved_poems_DB.bk_poem_id'))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))

    user = db.relationship("User", back_populates="comments")
    saved_poem = db.relationship("LibraryDB", back_populates="comments")


    def __repr__(self):
        return f'<Comment object poem_notes_id: {self.poem_notes_id} user_id: {self.user_id}>'


def LibraryDB(db.Model):
    """Creates a table for saving API-generated poems that 
    users wish to bookmark for future reading."""

    __tablename__ = "saved_poems_DB"

    bk_poem_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    api_url = db.Column(db.Text)
    title = db.Column(db.String(255))
    author = db.Column(db.String(150))
    full_text = db.Column(db.Text)

    comments = db.relationship("Comment", back_populates="saved_poem")

    def __repr__(self):
        return f'<LibraryDB object bk_poem_id: {self.bk_poem_id} 
        title: {self.title} author: {self.author}>'


def Mashup(db.Model):
    """Creates a table for API-generated mashup poems
    that the user wants to save."""

    __tablename__ = "saved_mashups"

    mashup_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    mashup_text = db.Column(db.Text)

    user = db.relationship("User", back_populates="mashups")
    components = db.relationship("MashupComponent", back_populates="mashup")

    def __repr__(self):
        return f'<Mashup object mashup_id: {self.mashup_id} user_id: {self.user_id}>'


def MashupComponent(db.Model):
    """Creates a table for components making up particular 
    mashup poems saved by the user."""

    __tablename__ = "mashup_components"

    component_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    mashup_id = db.Column(db.Integer,
                        db.ForeignKey("saved_mashup.mashup_id"))
    author_name = db.Column(db.String(100))
    source_poem = db.Column(db.String(100))

    mashup = db.relationship("Mashup", back_populates="components")

    def __repr__(self):
        return f'<MashupComponent object component_id: {self.component_id} 
        author_name: {self.author_name} source_poem: {self.source_poem}>'


def PromptDB(db.Model):
    """Database of poetry prompts to choose from."""

    __tablename__ = "prompts_DB"

    prompt_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    prompt_text = db.Column(db.String(255), unique=True)

    saved_prompts = db.relationship("SavedPrompt", back_populates="prompt")

    def __repr__(self):
        return f'<PromptDB object prompt_id: {self.prompt_id}>'


def SavedPrompt(db.Model):
    """Table allowing a user to bookmark a prompt they particularly like."""

    __tablename__ = "saved_prompts"

    saved_prompt_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    prompt_id = db.Column(db.Integer,
                        db.ForeignKey("prompts_DB.prompt_id"))

    prompt = db.relationship("PromptDB", back_populates="saved_prompts")
    user = db.relationship("User", back_populates="saved_prompts")

    def __repr__(self):
        return f'<SavedPrompt object saved_prompt_id: {self.saved_prompt_id} user_id: {self.user_id} prompt_id: {self.prompt_id}'

def SavedLinebreak(db.Model):
    """Table allowing user to save their poems with randomly generated
    line-breaks."""

    __tablename__ = "saved_userpoems"

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
    


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
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