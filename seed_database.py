"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# run these commands in the terminal
os.system('dropdb poetrytoolkitDB')
os.system('createdb poetrytoolkitDB')

# run these functions from model.py
model.connect_to_db(server.app)
model.db.create_all()

userX = model.User(username="userX", password="test", email="test@email.test")
poemX = model.Poem(api_url="xyz.com", title="good_poem_for_sure", author="somebody", full_text="lorem ipsum or whatever")

model.db.session.add(userX)
model.db.session.add(poemX)
model.db.session.commit()

commentX = model.Comment(user_notes="lorem ipsum i like it just fine", bk_poem_id=poemX.bk_poem_id, user_id=userX.user_id)

model.db.session.add(commentX)
model.db.session.commit()

poems_in_db = []

for n in range(10):
    api_url = f'xyz{n}.com'
    title = f'title{n}'
    author = f'author{n}'
    full_text = f'{n}\n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ut mollis turpis, condimentum semper eros. Nunc et tristique urna, sagittis scelerisque massa. Duis fringilla faucibus neque, nec hendrerit tellus elementum eget. In augue mauris, aliquet sit amet tempor nec, sagittis et sapien. Fusce iaculis arcu in luctus porttitor. Aenean dignissim mollis erat, sed efficitur dolor ultricies non. Sed non neque mattis, hendrerit felis non, pulvinar mauris. Donec nec bibendum leo. Aliquam eget eros sapien. Fusce nec leo a lectus volutpat suscipit. Vivamus nec libero luctus, condimentum quam eu, ullamcorper massa. Praesent a auctor tortor. Morbi euismod leo nec efficitur eleifend. Aenean feugiat, est nec ullamcorper scelerisque, magna odio interdum enim, eget fermentum sapien risus ut turpis.\n\nEtiam sit amet volutpat erat. Sed fringilla, tortor nec aliquam condimentum, enim mi consectetur elit, at varius libero nisl ac massa. Vestibulum suscipit, tellus eget rutrum imperdiet, orci nibh porttitor libero, et volutpat enim ipsum in dui. In hac habitasse platea dictumst. Nunc diam sem, viverra tincidunt ante consectetur, suscipit convallis tellus. Sed ac felis at diam lacinia pretium et ut leo. Ut vel vestibulum leo, at rutrum elit. Cras quis posuere metus. Vestibulum volutpat lectus sed ante tincidunt, id malesuada felis suscipit. Aliquam massa eros, gravida porttitor tempus a, dictum vel urna. In ornare diam vel consectetur faucibus. Ut eleifend posuere lacus eu finibus. '
    
    new_text = crud.create_bookmark(api_url=api_url, title=title, author=author, full_text=full_text)

    poems_in_db.append(new_text)
    model.db.session.add(new_text)

# model.db.session.add(poems_in_db)
model.db.session.commit()

# loop that generates ten user objects
for n in range(10):
    email = f'user{n}@test.com'
    username = f'user{n}'
    password = 'test'

    new_user = crud.create_user(username, email, password)

    # create 10 comments for the user
    for x in range(10):
        user_notes = f"{x}\nIt's pretty good I guess?"
        poem = choice(poems_in_db)
        # calls create_comment function to create new comment with filler text
        # and random poem choice and saves to variable rand_comment
        rand_comment = crud.create_comment(user_id=new_user.user_id, bk_poem_id=poem.bk_poem_id, user_notes=user_notes)
        # appends new_user.comments list with rand_comment object
        new_user.comments.append(rand_comment)

    model.db.session.add(new_user)

model.db.session.commit()  

