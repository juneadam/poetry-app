"""File to hold commonly useful modules for the server."""
import os

from jinja2 import StrictUndefined
from random import choice, randint, shuffle
from passlib.hash import argon2
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from functools import wraps

# ============ logged in decorator ============ #

def logged_in(route_function):
    
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


# ============ form easter egg ============= #

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

