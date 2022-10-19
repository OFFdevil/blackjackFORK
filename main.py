from flask import Flask, render_template, session, redirect
from objects.room import Room
import uuid
from util import check_auth
app = Flask(__name__)
app.config['SECRET_KEY'] = "hse_2022"


rooms = {}


@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    msg = session.get('message', '')

    if 'message' in session:
        session.pop('message')

    return render_template('index.html', user_data=session, message=msg)


@app.route('/start', methods=['GET'])
def start():
    check_auth()
    room_id = str(uuid.uuid4())
    rooms[room_id] = Room(room_id, user_id=session['user_id'])
    return redirect(f'/room/{room_id}')


@app.route('/room/<string:room_id>', methods=['GET'])
def playing_room(room_id):
    check_auth()

    if room_id not in rooms:
        return redirect('/')

    room = rooms[room_id]
    if room.check_auth(session['user_id']) is False:
        session['message'] = 'Permission to game is denied'
        return redirect('/')

    return render_template('game.html', room=room)


@app.route('/room/<string:room_id>/hit', methods=['GET'])
def hit(room_id):
    check_auth()

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
    check_auth()

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
    check_auth()

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



@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return 'OK'


app.run()