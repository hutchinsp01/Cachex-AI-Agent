from numpy import sign
from irrationalAgents.basicBoard import _SWAP_PLAYER

def pieceAdvantage(state, player):
    playerCount = 0
    opponentCount = 0

    opponent = _SWAP_PLAYER[player]

    for i in range (0, len(state._data)):
            for j in range(0, len(state._data)):
                if state._data[i][j] == player:
                    playerCount += 1
                if state._data[i][j] == opponent:
                    opponentCount += 1

    return playerCount - opponentCount

def avgDistanceFromCentre(state, player):
    playerSum = 0
    playerCount = 0

    centre = len(state._data) / 2
    centre = (centre, centre)

    for i in range (0, len(state._data)):
            for j in range(0, len(state._data)):
                if state._data[i][j] == player:
                    playerCount += 1
                    playerSum += manhatten_distance((i, j), centre)

    playerTotal =  (playerSum / playerCount) if playerCount != 0 else 0
    if playerTotal == 0:
        return 0
    
    return 1 / playerTotal

def manhatten_distance(cur, goal):
    dx = cur[0] - goal[0]
    dy = cur[1] - goal[1]

    if sign(dx) == sign(dy):
        return abs(dx + dy)
    
    return max(abs(dx), abs(dy))