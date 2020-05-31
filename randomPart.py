import socketio
import random
import numpy as np

sio = socketio.Client()

class Timbiriche:
    def __init__(self):
        self.username = ""
        self.tid = ""
        self.gameID = ""
        self.board = []
        self.player_id = 0
        self.oponnent_id = 0
        self.win = 0
        self.lost = 0

@sio.on('connect')
def onConnect():
    print('Connection')
    sio.emit('signin', {
        'user_name': timbiriche.username,
        'tournament_id': timbiriche.tid,
        'user_role': 'player'
    }) 

@sio.on('ready')
def onReady(server):
    timbiriche.player_id = server['player_turn_id']
    timbiriche.gameID = server['game_id']
    timbiriche.board = server['board']

    movement = random.randint(0, 1)
    line = random.randint(0, 29)

    while int(timbiriche.board[movement][line]) != 99:
        movement = random.randint(0, 1)
        line = random.randint(0, 29)

    sio.emit('play', {
        'player_turn_id': timbiriche.player_id,
        'tournament_id': timbiriche.tid,
        'game_id': timbiriche.gameID,
        'movement': [movement, line]
    })

@sio.on('finish')
def on_finish(server):
    print('The game', timbiriche.gameID, 'has finished.')

    restart()

    if server['player_turn_id'] == server['winner_turn_id']:
        print("Ganaste :D")
        timbiriche.win += 1
    else:
        print("Perdiste :(")
        timbiriche.lost += 1

    sio.emit('player_ready', {
        'tournament_id': timbiriche.tid,
        'game_id': timbiriche.gameID,
        'player_turn_id': timbiriche.player_id
    })

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

def restart():
    row = np.ones(30) * 99
    timbiriche.board = [np.ndarray.tolist(row), np.ndarray.tolist(row)]


timbiriche = Timbiriche()
# timbiriche.username = input("Ingrese su usuario: ")
timbiriche.username = 'RANDOM'
# timbiriche.tid = input("Ingrese el Tournament ID: ")
timbiriche.tid = '1'

# host = input("Ingrese el host: ")
host = 'http://localhost:4000'

sio.connect(host)
