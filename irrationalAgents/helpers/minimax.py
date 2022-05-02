from numpy import Infinity
from irrationalAgents.basicBoard import _SWAP_PLAYER, _TOKEN_MAP_OUT
from irrationalAgents.constants import MAX_DEPTH
from irrationalAgents.helpers.pieces import pieceAdvantage
import copy


def minimax(state, depth, action, curPlayer, ourPlayer):

    if action != None:
        state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])

    # [best row, best col, best score]
    if curPlayer == ourPlayer:
        best = [-1, -1, -Infinity]
    else:
        best = [-1, -1, +Infinity]
    

    if depth == MAX_DEPTH:
        # score = evaluate(state)
        return [-1, -1, evaluate(state, curPlayer)]


    # pruned_state = prune(state)
    # for hex in pruned_state:

    for hex in empty_hexes(state):
        x, y = hex[0], hex[1] 
        action = ("PLACE", x, y)
        saveState = copy.deepcopy(state._data)
        score = minimax(state, depth + 1, action, _SWAP_PLAYER[curPlayer], ourPlayer)
        state.revert_state(saveState)
        score[0], score[1] = x, y 

        if curPlayer == ourPlayer:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

def empty_hexes(state):
    empty_hexes = []
    for i in range (0, state.n):
            for j in range(0, state.n):
                    if state._data[i][j] == 0:
                        empty_hexes.append((i, j))
    return empty_hexes

def evaluate(state, player):
    score = pieceAdvantage(state, player)
    return score



