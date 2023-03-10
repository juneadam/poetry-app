"""Script to seed database."""

import os
# import json
from random import choice, randint
# from datetime import datetime
from passlib.hash import argon2

import crud
import model
import server
# print("AHHHHHHHHHHHHH")

def seed_database():
    """seeds all test data."""

    test_pw = os.environ['test_pw']
    password = argon2.hash(test_pw)
    userX = model.User(username="userX", password=password, email="test@email.test")
    poemX = model.Poem(title="good_poem_for_sure", author="somebody")

    model.db.session.add(userX)
    model.db.session.add(poemX)
    model.db.session.commit()

    commentX = model.Comment(user_notes="lorem ipsum i like it just fine", bk_poem_id=poemX.bk_poem_id, user_id=userX.user_id)
    model.db.session.add(commentX)
    model.db.session.commit()

    new_lineX = crud.create_bookmark_lines(1, ["It is June.", "The woods are damp."])
    model.db.session.add_all(new_lineX)
    model.db.session.commit()

    new_promptX = crud.create_prompt("What's the name of tomorrow? Write an ode.")
    model.db.session.add(new_promptX)
    model.db.session.commit()    

    new_prompt_responseX = crud.save_prompt_response(1, 1, 'filler_text')
    model.db.session.add(new_prompt_responseX)
    model.db.session.commit()

    new_mashupX = crud.create_mashup(1, 'mashupTitleX', 'userX')
    model.db.session.add(new_mashupX)
    model.db.session.commit()


    # Creates 10 poem objects to test the database.
    poems_in_db = []

    for n in range(10):
        title = f'title{n}'
        author = f'author{n}'
        
        new_text = crud.create_bookmark(title=title, author=author)

        poems_in_db.append(new_text)

    model.db.session.add_all(poems_in_db)
    model.db.session.commit()

    # Creates 10 user objects and 4 comments for each user to test the database.
    
    # loop that generates ten user objects
    for n in range(10):
        email = f'user{n}@test.com'
        username = f'user{n}'
        test_pw = os.environ['test_pw']
        hashed_pw = argon2.hash(test_pw)

        new_user = crud.create_user(username, email, password=hashed_pw)

        # create 4 comments for the user
        for x in range(4):
            user_notes = f"{x}\nIt's pretty good I guess?"
            poem = choice(poems_in_db)
            # calls create_comment function to create new comment with filler text
            # and random poem choice and saves to variable rand_comment
            rand_comment = crud.create_comment(user_id=new_user.user_id, bk_poem_id=poem.bk_poem_id, user_notes=user_notes)
            # appends new_user.comments list with rand_comment object
            new_user.comments.append(rand_comment)

        model.db.session.add(new_user)

    model.db.session.commit()  

    # Creates 5 mashup objects and 4 lines for each for testing the database.

    # loop to generate 5 mashup objects
    for n in range(5):
        user_id = randint(1,10)
        mashup_title = f'Title of Mashup{n}'
        mashup_author = f'Author of Mashup{n}'

        new_mashup = crud.create_mashup(user_id=user_id, mashup_title=mashup_title, mashup_author=mashup_author)

        model.db.session.add(new_mashup)
        model.db.session.commit()

        #create 4 lines for each mashup
        lines = []
        for x in range(4):
            line = (f'source_author{n}', f'source_poem{n}', f'this_is_a_line_of_text{n}')
            lines.append(line)
        mashup_id = new_mashup.mashup_id
        new_mashup_lines = crud.create_mashup_lines(mashup_id=mashup_id, lines=lines)


        model.db.session.add_all(new_mashup_lines)
        model.db.session.commit()


    # Adds the prompts list to the database for testing.

    # database of poetry prompts

    PROMPTS = ["Why are my shoes wet?",
                "Write down the first 14 words you can think of. Write a sonnet using them - start or end a line with each, or incorporate them into each line.",
                "A haiku is 3 lines, with 5, 7, and 5 syllables each. Pick a number 1-10 to choose a number of lines, then continue picking numbers 1-10 to choose the number of syllables for each line.",
                "I haven't slept in weeks.",
                "Why is the sky on fire?",
                "Pick up a book near you, turn to page 28, and pick the first word on the page. Use it to start a poem.",
                "Hold yourself accountable for one crime.",
                "Forgive yourself for one crime.",
                "Tell a story about the last great joy you felt.",
                "Find a poem you like and replace it one word at a time until it is new.",
                "Where did you come from? Do not name a place.",
                "Write six lines that don't have anything to do with each other. Rearrange them until they do.",
                "Are you warm enough today? What do you need to keep warm?"
                ]

    prompt_objects = []

    for prompt in PROMPTS:
        
        add_prompt = crud.create_prompt(prompt)

        prompt_objects.append(add_prompt)


    model.db.session.add_all(prompt_objects)
    model.db.session.commit()

    return


if __name__ == "__main__":
    # run these commands in the terminal
    os.system('dropdb poetrytoolkitDB')
    os.system('createdb poetrytoolkitDB')

    # run these functions from model.py
    model.connect_to_db(server.app)
    server.app.app_context().push()
    model.db.create_all()

    seed_database()
