from flask import Flask, render_template, session, redirect, request
from objects.room import Room
import uuid
from util import check_auth

import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


app = Flask(__name__)
app.config['SECRET_KEY'] = randomword(40)


rooms = {}

users = {}


class User:
    def __init__(self, login, password, balance=123) -> None:
        self.login = login
        self.password = password
        self.balance = balance


@app.route('/')
def index():
    if not check_auth():
        return redirect('/login')

    msg = session.get('message', '')

    if 'message' in session:
        session.pop('message')

    return render_template('index.html', user_data=users[session['user_id']], message=msg)


@app.route('/start', methods=['GET', 'POST'])
def start():
    if not check_auth():
        return redirect('/login')
    
    user = users[session['user_id']]
    
    bet = int(request.form['bet'])

    if user.balance < bet:
        session['message'] = 'Your balance is less than your bet!'
        return redirect('/')


    room_id = str(uuid.uuid4())
    rooms[room_id] = Room(room_id, bet, user_id=session['user_id'], user=user)
    return redirect(f'/room/{room_id}')


@app.route('/room/<string:room_id>', methods=['GET'])
def playing_room(room_id):
    if not check_auth():
        return redirect('/login')

    if room_id not in rooms:
        return redirect('/')

    room = rooms[room_id]
    if room.check_auth(session['user_id']) is False:
        session['message'] = 'Permission to game is denied'
        return redirect('/')

    return render_template('game.html', room=room)


@app.route('/room/<string:room_id>/hit', methods=['GET'])
def hit(room_id):
    if not check_auth():
        return redirect('/login')

    if room_id not in rooms:
        return redirect('/')

    room = rooms[room_id]
    if room.check_auth(session['user_id']) is False:
        session['message'] = 'Permission to game is denied'
        return redirect('/')

    room.hit()

    return redirect(f'/room/{room_id}')


@app.route('/room/<string:room_id>/stand', methods=['GET'])
def stand(room_id):
    if not check_auth():
        return redirect('/login')

    if room_id not in rooms:
        return redirect('/')

    room = rooms[room_id]
    if room.check_auth(session['user_id']) is False:
        session['message'] = 'Permission to game is denied'
        return redirect('/')

    room.stand()
    return redirect(f'/room/{room_id}')


@app.route('/room/<string:room_id>/quit', methods=['GET'])
def quit(room_id):
    if not check_auth():
        return redirect('/login')

    if room_id not in rooms:
        return redirect('/')

    room = rooms[room_id]
    if room.check_auth(session['user_id']) is False:
        session['message'] = 'Permission to game is denied'
        return redirect('/')
    room.quit()
    return redirect(f'/room/{room_id}')


@app.errorhandler(404)
def page_not_found(_):
    return render_template('page_not_found.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if check_auth():
        return redirect('/error')
    
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form['login']
        password = request.form['password']
    
        if login in users:
            user = users[login]

            if user.password == password:
                session['user_id'] = login
                return redirect('/')
            else:
                return render_template('login.html', message='password is invalid') 
        else:
            users[login] = User(login, password)
            session['user_id'] = login
            return redirect('/') 

@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return 'OK'


app.run(port=1234)