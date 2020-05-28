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

    def max_alpha_beta(self, alpha, beta):
        maxv = -2

        px = None
        py = None

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if int(self.board[i][j]) == 99:
                    self.board[i][j] = self.player_id
                    (m, min_i, min_j) = self.min_alpha_beta(alpha, beta)

                    print('max:', (m, min_i, min_j))
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j

                    self.board[i][j] = 99

                    if maxv >= beta:
                        return (maxv, px, py)
                    
                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta):
        minv = 2

        qx = None
        qy = None

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if int(self.board[i][j]) == 99:
                    self.board[i][j] = self.oponnent_id
                    (m, max_i, max_j) = self.min_alpha_beta(alpha, beta)
                    print('min:', (m, max_i, max_j))

                    if m < minv:
                        minv = m
                        qx = i
                        qy = j

                    self.board[i][j] = 99

                    if minv <= alpha:
                        return (minv, qx, qy)
                    
                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

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
    print('Ready')
    print(server)

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
    else:
        print("Perdiste :(")

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
timbiriche.tid = input("Ingrese el Tournament ID: ")

host = input("Ingrese el host: ")

sio.connect(host)





