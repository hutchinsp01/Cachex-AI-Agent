from numpy import sign
from irrationalAgents1.basicBoard import _SWAP_PLAYER
from irrationalAgents1.basicBoard import Board
from itertools import cycle
import numpy as np

def pieceAdvantage(state: Board, player: int):
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

def avgDistanceFromCentre(state: Board, player: int):
    playerSum = 0
    playerCount = 0

    centre = (len(state._data) - 1) / 2
    centre = (centre, centre)

    for i in range (0, len(state._data)):
        for j in range(0, len(state._data)):
            if state._data[i][j] == player:
                playerCount += 1
                playerSum += manhatten_distance((i, j), centre)

    playerTotal =  (playerSum / playerCount) if playerCount != 0 else 0
    
    return playerTotal

def manhatten_distance(cur: tuple, goal: tuple):
    dx = cur[0] - goal[0]
    dy = cur[1] - goal[1]

    if sign(dx) == sign(dy):
        return abs(dx + dy)
    
    return max(abs(dx), abs(dy))

def triangle_structures(state: Board, player: int) -> int:
    '''
    Evaluates the number of triangle structures present for a player.
    These are desirable as they are less susceptible to capture.
    '''
    
    triangleCount = 0
    for coord in state.occupied_hexes:
        if state._data[coord] == player:
            neighbours = state._coord_neighbours(coord)
            neighbourCycle = cycle(neighbours)
            curNeighbour = next(neighbourCycle)
            
            # go through all neighbours, minus the first one
            for k in range(len(neighbours)):
                (x1, y1) = curNeighbour
                nextNeighbour = next(neighbourCycle)
                (x2, y2) = nextNeighbour
                if (state._data[x1][y1] == player) and (state._data[x2][y2] == player):
                    triangleCount += 1

                curNeighbour = nextNeighbour
                
    return triangleCount