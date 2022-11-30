from flask import redirect, session


def check_auth():
    return 'user_id' in session
    