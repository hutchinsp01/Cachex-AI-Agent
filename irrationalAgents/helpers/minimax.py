from numpy import Infinity
import numpy as np
from irrationalAgents.basicBoard import _SWAP_PLAYER, _TOKEN_MAP_OUT
from irrationalAgents.constants import MAX_DEPTH
from irrationalAgents.helpers.pieces import manhatten_distance, pieceAdvantage, avgDistanceFromCentre, triangle_structures
from irrationalAgents.helpers.evaluation import dijkstraEvalScore
import copy


def minimax(state, depth : int, action : tuple, a : float, b : float, curPlayer : int, ourPlayer: int) -> float:
    # Print calls to help me figure out how it was working :)
    # print("Depth = " + str(depth))
    # print("Minimaxing move: Player " + str(curPlayer) + " " + str(action))
    # print("State:")
    # print(state._data)
    
    # Check if victory has been achieved. If so, we don't need to keep making moves on this state.
    # victory = 0
    # if state.turns_taken >= (2 * state.n - 1) and action is not None:
    #     victory = check_winner(state, action, curPlayer, ourPlayer)
    #     if victory == 1 or victory == -1:
    #         return [action[1], action[2], victory]

    # If we have hit max depth for minimax (and there's no victory), it's time to evaluate the board state.
    if depth == MAX_DEPTH:
        return [-1, -1, evaluate(state, ourPlayer, action)]

    # If we haven't hit max depth and victory hasn't been achieved, time to explore deeper.
    if curPlayer == ourPlayer:
        # Best outcome starts out at -inf w.r.t our player
        best = [-1, -1, -Infinity]
        
        for hex in empty_hexes(state):
            # place piece in hex, then run minimax on the resulting state
            x, y = hex[0], hex[1]
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            score = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer)
            
            # revert the action, so that a new one can be performed for the next hex
            state.undo_move(move)
            
            # if eval score surpasses the current best, we have a new best move
            score[0], score[1] = x, y
            if score[2] > best[2]:
                best = score

            # if our maximizing player hits a score that is greater than what the minimizing player will consider, break. This board state is now irrelevant and the rest of the possible moves are pruned.
            if best[2] >= (b):
                break
            
            # update alpha so moves further down the minimax tree can use it as a reference
            a = max(a, best[2])
    else:
        # Best outcome starts at inf w.r.t our player
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
            
            if best[2] <= (a) :
                break
            
            b = min(b, best[2])

    if best[0] == -1 or best[1] == -1:
        empty_hex = empty_hexes(state)[0]
        best[0], best[1] = empty_hex[0], empty_hex[1]

    # print("Given state:")
    # print_state(state._data)
    # print(f"The best move for {curPlayer} is {str(best)}")
    return best

def check_winner(state, action, curPlayer: int) -> int:
    '''
    Checks if victory has been achieved. 
    Returns -1 if loss, 0 if no victory, 1 if victory, w.r.t ourPlayer.
    Code borrowed from game.py in referee module provided by COMP30024 tutors.
    '''
    # axis is 0 for red, 1 for blue
    axis = 0 if curPlayer == 1 else 1

    _, r, q = action
    reachable = state.connected_coords((r, q))
    axis_vals = [coord[axis] for coord in reachable]
    
    if min(axis_vals) == 0 and max(axis_vals) == state.n - 1:
        # we have a win for curPlayer!
        return 1
    
    return 0

def empty_hexes(state):
    '''
    Adds nodes to minimax search queue based upon empty hexes on the board. 
    Does not attempt to achieve optimal ordering to enhance effectiveness of a-b pruning
    '''
    empty_hexes = []
    for i in range (0, state.n):
            for j in range(0, state.n):
                    if state._data[i][j] == 0:
                        empty_hexes.append((i, j))

    return sorted(empty_hexes, key=lambda x: manhatten_distance(x, (state.n//2, state.n//2)), reverse=True )


def evaluate(state, player: int, action: tuple):
    '''
    Evaluation or utility function. 
    Returns a value for the 'desirability' of a board state based upon an evaluation of certain features.
    '''

    dijkstraScore = dijkstraEvalScore(player, state)
    avgDistanceScore = -1 * avgDistanceFromCentre(state, player)
    pieceAdvantageScore = pieceAdvantage(state, player)
    triangeStructureScore = triangle_structures(state, player) / 3
    
    score = 3 * dijkstraScore + avgDistanceScore + 2 * pieceAdvantageScore + triangeStructureScore

    # print("EVAL! Action: " + str(action) + ". with respect to player " + str(player) + ". Score = " + str(np.arctan(score)/(np.pi/2)) + ".")
    # print(f"Dijkstra: {dijkstraScore}, Distance: {avgDistanceScore}, Piece Advantage: {pieceAdvantageScore}, Triangle Structure: {triangeStructureScore}")
    # print("State:")
    # print_state(state._data)
    
    # Normalise the score so that it lies in the range [-1, 1]. Note that the extremes are only possible in the case of victory or loss.
    return np.arctan(score)/(np.pi/2)

def print_state(data):
    '''
    Convenient function for printing state that doesn't need the provided render aesthetic.
    Provides a better visual representation of the board than a 2D array.
    '''
    indentDepth = len(data)
    for row in data[::-1]:
        indent = indentDepth * " "
        print(indent + str(row))
        indentDepth -= 1
    return



