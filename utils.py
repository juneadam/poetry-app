"""File to hold commonly useful modules for the server."""
import os

from jinja2 import StrictUndefined
from random import choice, randint, shuffle
from passlib.hash import argon2
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from functools import wraps

# ============ logged in decorators ============ #

def logged_in(route_function):
    """Decorator for checking if a user is logged in, for rendering routes."""
    
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            flash('You must be logged in to access this feature.')
            return redirect('/')
        else:
            route = route_function(*args, **kwargs)
            return route
    
    return wrapper


def logged_in_JSON(route_function):
    """Decorator for checking if a user is logged in, for JSON routes."""

    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return 'not logged in'
        else:
            route = route_function(*args, **kwargs)
            return route
        
    return wrapper


# ============ poems: url payload generator ============#

def get_payload(author, title, lines, linecount):
    """checks to see if user is using certain parameters, and if so,
    adds a tuple to the payload list to be formatted into a usable URL
    for an API call."""

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

    return (input_fields, output_fields)


# ============ mashups: linecount range modifier ============ #

def range_modifier(linecount):
    """modifier to add deeper selection criteria to smaller linecount datasets"""

    plus_amount = 0
    if linecount < 4:
        plus_amount = 5
    else:
        plus_amount = 2

    return plus_amount
        


# ============ mashups: poem form easter egg ============= #

def form_easter_egg(linecount):
    """Easter egg that adds line-specific form names to mashup titles."""
    
    if linecount == 3:
        return "Haiku: "
    if linecount == 5:
        return "Limerick: "
    if linecount == 14:
        return "Sonnet: "
    if linecount == 19:
        return "Villanelle: "
    if linecount == 100:
        return "Cento: "


