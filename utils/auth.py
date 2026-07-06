from functools import wraps
from flask import session, redirect


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user" not in session:
            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


def role_required(role):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if session.get("role") != role:
                return redirect("/login")

            return func(*args, **kwargs)

        return wrapper

    return decorator