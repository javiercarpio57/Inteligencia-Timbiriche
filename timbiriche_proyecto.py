import socketio
# import random
import numpy as np
import math

sio = socketio.Client()

class Timbiriche:
    def __init__(self):
        self.username = ""
        self.tid = ""
        self.gameID = ""
        self.board = []
        self.player_id = 0
        self.oponnent_id = 0


def minimax(move, board, depth, alpha, beta, idPlayer):
    # print('DEPTH:', depth)
    if depth == 0 or 99 not in np.asarray(board).reshape(-1):
        return getPoints(board, idPlayer, move), move

    if idPlayer == timbiriche.player_id:
        
        maxEval = -math.inf

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 99:
                    move = (i, j)
                    board[i][j] = idPlayer

                    value, _ = minimax(move, board, depth - 1, alpha, beta, (idPlayer % 2) + 1)

                    board[i][j] = 99
                    maxEval = max(maxEval, value)
                    alpha = max(alpha, value)

                    if beta <= alpha:
                        break
        return maxEval, move

    else:
        minEval = math.inf

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 99:
                    move = (i, j)
                    board[i][j] = idPlayer

                    value, _ = minimax(move, board, depth - 1, alpha, beta, (idPlayer % 2) + 1)

                    minEval = min(minEval, value)
                    beta = min(beta, value)

        return minEval, move


def getPoints(board, playerNumber, move):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    punteoInicial = 0
    punteoFinal = 0

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoInicial = punteoInicial + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0

    # return punteoFinal - punteoInicial
    return punteoInicial

def humanBoard(board):
    resultado = ''
    acumulador = 0

    for i in range(int(len(board[0])/5)):
        if board[0][i] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+6] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+12] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+18] == 99:
            resultado = resultado + '*   '
        else:
            resultado = resultado + '* - '
        if board[0][i+24] == 99:
            resultado = resultado + '*   *\n'
        else:
            resultado = resultado + '* - *\n'

        if i != 5:
            for j in range(int(len(board[1])/5)):
                if board[1][j + acumulador] == 99:
                    resultado = resultado + '    '
                else:
                    resultado = resultado + '|   '
            acumulador = acumulador + 6
            resultado = resultado + '\n'

    return resultado

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

    # print('MY ID:', server['player_turn_id'])

    print(humanBoard(server['board']))

    _, move = minimax(None, server['board'], 3, -math.inf, math.inf, server['player_turn_id'])

    # print(move)
    movement = move[0]
    line = move[1]

    while int(timbiriche.board[movement][line]) != 99:
        _, move = minimax(None, server['board'], 3, -math.inf, math.inf, server['player_turn_id'])
        movement = move[0]
        line = move[1]


    print('MOVIMIENTO:', move)

    sio.emit('play', {
        'player_turn_id': server['player_turn_id'],
        'tournament_id': timbiriche.tid,
        'game_id': server['game_id'],
        'movement': [movement, line]
    })

@sio.on('finish')
def on_finish(server):
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
# timbiriche.username = input("Ingrese su usuario: ")
timbiriche.username = 'INTELIGENCIA'
timbiriche.tid = input("Ingrese el Tournament ID: ")

host = input("Ingrese el host: ")

sio.connect(host)
