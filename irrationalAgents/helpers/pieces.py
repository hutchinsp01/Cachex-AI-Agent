from numpy import sign
from irrationalAgents.basicBoard import _ADD, _CAPTURE_PATTERNS, _SWAP_PLAYER
from irrationalAgents.basicBoard import Board
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

def opponentEdge(state: Board, player: int) -> int:

    blueScore = [state._data[x[0]][x[1]] for x in state.red_end].count(2)
    blueScore += [state._data[x[0]][x[1]] for x in state.red_start].count(2)

    redScore = [state._data[x[0]][x[1]] for x in state.blue_end].count(1)
    redScore += [state._data[x[0]][x[1]] for x in state.blue_start].count(1)

    if player == 1:
        return redScore - blueScore

    return blueScore - redScore

def islandCount(state: Board, player: int) -> int:
    blueScore = 0
    redScore = 0

    for (x,y) in state.occupied_hexes:
        for pattern in _CAPTURE_PATTERNS:
                coords = [_ADD((x,y), s) for s in pattern]
                # No point checking if any coord is outside the board!
                if all(map(state.inside_bounds, coords)):
                    if state._data[x][y] == 1:
                        if [x for x in coords].count(1) == 0:
                             redScore += 1
                    if state._data[x][y] == 2:
                        if [x for x in coords].count(2) == 0:
                            blueScore += 1        

    if player == 1:
        return redScore - blueScore

    return blueScore - redScore

    

