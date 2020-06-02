import socketio
import numpy as np
from math import inf as infinity
from utilities import *
import time

sio = socketio.Client()

class Timbiriche:
    def __init__(self):
        self.username = ""
        self.tid = ""
        self.gameID = ""
        self.board = []
        self.player_id = None
        self.oponnent_id = None
        self.lastBoard = []
        self.look = 0
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
    print()
    print(humanBoard(server['board']))

    start_time = time.time()
    move = suggestMove(server['board'], server['player_turn_id'], timbiriche.look)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    print('ENVIADO')
    sio.emit('play', {
        'player_turn_id': server['player_turn_id'],
        'tournament_id': timbiriche.tid,
        'game_id': server['game_id'],
        'movement': [move[0], move[1]]
    })

@sio.on('finish')
def on_finish(server):
    restart()

    if server['player_turn_id'] == server['winner_turn_id']:
        timbiriche.win += 1
        print("Ganaste :D (", timbiriche.win, '-', timbiriche.lost, ")")
    else:
        timbiriche.lost += 1
        print("Perdiste :( (", timbiriche.win, '-', timbiriche.lost, ")")

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
timbiriche.username = input("Ingrese su usuario: ")
# timbiriche.username = 'Javi'
# timbiriche.tid = input("Ingrese el Tournament ID: ")
timbiriche.tid = '1'
timbiriche.look = int(input('LOOK AHEAD: '))
# timbiriche.look = 2

# host = input("Ingrese el host: ")
host = 'http://localhost:4000'

sio.connect(host)
