from numpy import Infinity
from irrationalAgents.basicBoard import _SWAP_PLAYER
from irrationalAgents.constants import MAX_DEPTH


def minimax(state, depth, curPlayer, ourPlayer):

    # [best row, best col, best score]
    if curPlayer == ourPlayer:
        best = [-1, -1, -Infinity]
    else:
        best = [-1, -1, +Infinity]
    

    if depth == MAX_DEPTH:
        # score = evaluate(state)
        return [-1, -1, 0]


    # pruned_state = prune(state)
    # for hex in pruned_state:

    for hex in empty_hexes(state):
        x, y = hex[0], hex[1] 
        state._data[x][y] = curPlayer
        score = minimax(state, depth + 1, _SWAP_PLAYER[curPlayer], ourPlayer)
        state._data[x][y] = 0
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



