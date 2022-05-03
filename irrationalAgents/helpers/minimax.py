from numpy import Infinity
from irrationalAgents.basicBoard import _SWAP_PLAYER, _TOKEN_MAP_OUT
from irrationalAgents.constants import MAX_DEPTH
from irrationalAgents.helpers.pieces import pieceAdvantage, avgDistanceFromCentre
from irrationalAgents.helpers.evaluation import dijkstraEvalScore
import copy


def minimax(state, depth, action, a, b, curPlayer, ourPlayer):
    
    if depth == MAX_DEPTH:
        return [-1, -1, evaluate(state, curPlayer)]

    if curPlayer == ourPlayer:
        best = [-1, -1, -Infinity]
        for hex in empty_hexes(state):
            x, y = hex[0], hex[1]
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            score = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer)
            state.undo_move(move)
            score[0], score[1] = x, y
            if score[2] > best[2]:
                best = score
            if best[2] >= (b - 1):
                break;
            a = max(a, best[2])
    else:
        best = [-1, -1, Infinity]
        for hex in empty_hexes(state):
            x, y = hex[0], hex[1]
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            score = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer)
            state.undo_move(move)
            score[0], score[1] = x, y
            if score[2] < best[2]:
                best = score
            if best[2] <= (a + 1) :
                break;
            b = max(b, best[2])

    if best[0] == -1 or best[1] == -1:
        empty_hex = empty_hexes(state)[0]
        best[0], best[1] = empty_hex[0], empty_hex[1]

    return best


def empty_hexes(state):
    empty_hexes = []
    for i in range (0, state.n):
            for j in range(0, state.n):
                    if state._data[i][j] == 0:
                        empty_hexes.append((i, j))
    return empty_hexes

def evaluate(state, player: int):
    score = 2 * dijkstraEvalScore(player, state) + avgDistanceFromCentre(state, player) + 2 * pieceAdvantage(state, player)
    return score



