import numpy as np
from math import inf as infinity
import random

def getPossibleMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if int(board[i][j]) == 99:
                moves.append((i, j))

    random.shuffle(moves)
    return moves

def minimax(board, move, depth, isMe, myId, alpha, beta):
    idPlayerPlaying = myId if isMe else (myId % 2) + 1
    p = heuristica(board, move, idPlayerPlaying, not isMe)

    if depth == 0 or 99 not in np.asarray(board).reshape(-1) or p != 0:
        return heuristica(board, move, idPlayerPlaying, not isMe)

    board, _ = doMove(board, move, idPlayerPlaying, isMe)
    possibleMoves = getPossibleMoves(board)

    if isMe:
        maxEval = -infinity
        
        for movimiento in possibleMoves:
            value = minimax(board, movimiento, depth - 1, False, idPlayerPlaying, alpha, beta)

            maxEval = max(maxEval, value)
            alpha = max(alpha, value)

            if beta <= alpha:
                break

        board[move[0]][move[1]] = 99
        return maxEval

    else:
        minEval = infinity
        
        for movimiento in possibleMoves:
            value = minimax(board, movimiento, depth - 1, True, idPlayerPlaying, alpha, beta)

            minEval = min(minEval, value)
            beta = min(beta, value)

            if beta <= alpha:
                break

        board[move[0]][move[1]] = 99
        return minEval

def suggestMove(board, myId, lookahead):
    bestScore = -infinity
    possibleMoves = []

    possible = getPossibleMoves(board)
    suma = int(np.sum(board))
    if suma == ((99 * len(board[0])) + (99 * len(board[1]))) or suma == ((99 * len(board[0])) + (99 * (len(board[1]) - 1))):
        return random.choice(possible)
    else:
        for movimiento in possible:
            score = minimax(board, movimiento, int(lookahead), False, int(myId), -infinity, infinity)

            if score > bestScore:
                bestScore = score
                possibleMoves.clear()

            if score >= bestScore:
                possibleMoves.append(movimiento)

    return random.choice(possibleMoves)

def doMove(oldBoard, move, playerNumber, isMe):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    board = list(map(list, oldBoard))

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

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21
    
    return (board, punteoFinal - punteoInicial) if isMe else (board, (-1) * (punteoFinal - punteoInicial))

def heuristica(oldBoard, move, playerNumber, isMe):
    EMPTY = 99
    FILL = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2
    N = 6

    board = list(map(list, oldBoard))

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

    board[move[0]][move[1]] = FILL

    acumulador = 0
    contador = 0

    for i in range(len(board[0])):
        if ((i + 1) % N) != 0:
            if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
                punteoFinal = punteoFinal + 1
            acumulador = acumulador + N
        else:
            contador = contador + 1
            acumulador = 0
    
    if punteoInicial < punteoFinal:
        if playerNumber == 1:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP12
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP11
        elif playerNumber == 2:
            if (punteoFinal - punteoInicial) == 2:
                board[move[0]][move[1]] = FILLEDP22
            elif (punteoFinal - punteoInicial) == 1:
                board[move[0]][move[1]] = FILLEDP21

    return punteoFinal - punteoInicial if isMe else (-1) * (punteoFinal - punteoInicial)

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


