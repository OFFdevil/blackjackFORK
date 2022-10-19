from flask import redirect, session


def check_auth():
    if 'user_id' not in session:
        return redirect('/')