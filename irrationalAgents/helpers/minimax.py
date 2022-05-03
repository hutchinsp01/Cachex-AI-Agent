from numpy import Infinity
from irrationalAgents.basicBoard import _SWAP_PLAYER, _TOKEN_MAP_OUT
from irrationalAgents.constants import MAX_DEPTH
from irrationalAgents.helpers.pieces import pieceAdvantage
from irrationalAgents.helpers.evaluation import dijkstraEvalScore
import copy


def minimax(state, depth, action, a, b, curPlayer, ourPlayer):
    
    if depth == MAX_DEPTH:
        return evaluate(state, curPlayer)

    if curPlayer == ourPlayer:
        value = -Infinity
        for hex in empty_hexes(state):
            x, y = hex[0], hex[1] 
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            newValue = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer)
            value = max(value, newValue)
            state.undo_move(move)
            if value >= b:
                break;
            a = max(a, value)
        if depth == 0:
            return (x, y)
        return value
    else:
        value = +Infinity
        for hex in empty_hexes(state):
            x, y = hex[0], hex[1] 
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            newValue = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer)
            value = min(value, newValue)
            state.undo_move(move)
            if value <= a:
                break;
            b = min(b, value)
        return value 

def empty_hexes(state):
    empty_hexes = []
    for i in range (0, state.n):
            for j in range(0, state.n):
                    if state._data[i][j] == 0:
                        empty_hexes.append((i, j))
    return empty_hexes

def evaluate(state, player: int):
    score = dijkstraEvalScore(player, state)
    return score



