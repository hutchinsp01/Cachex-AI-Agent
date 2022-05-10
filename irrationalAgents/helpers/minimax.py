from time import process_time
import time
from numpy import Inf, Infinity
import numpy as np
from irrationalAgents.basicBoard import _SWAP_PLAYER, _TOKEN_MAP_OUT
from irrationalAgents.helpers.pieces import manhatten_distance, opponentEdge, pieceAdvantage, avgDistanceFromCentre, triangle_structures
from irrationalAgents.helpers.evaluation import dijkstraEvalScore
import copy


def minimax(state, depth : int, action : tuple, a : float, b : float, curPlayer : int, ourPlayer: int, maxDepth: int) -> float:
    # Print calls to help me figure out how it was working :)
    # print("Depth = " + str(depth))
    # print("Minimaxing move: Player " + str(curPlayer) + " " + str(action))
    # print("State:")
    # print_state(state._data)
    # print("Occupied hexes: " + str(state.occupied_hexes))
    # print("Turns: " + str(state.turns_taken))
    # print("Degrees:")
    # print_state(state.hex_degrees)
    
    # Check if victory has been achieved. If so, we don't need to keep making moves on this state.
    victory = 0
    if state.turns_taken >= (2 * state.n - 1) and action is not None:
        # print(f"Assessing victory for player {curPlayer}  wrt {ourPlayer}")
        victory = check_winner(state, action, curPlayer, ourPlayer)
        if victory == 1 or victory == -1:
            return [action[1], action[2], Inf * victory]

    if ((state.greedyLimit - (state.totalTime + (time.process_time() - state.moveStart))) <= 0 ):
        maxDepth = 1

    # If we have hit max depth for minimax (and there's no victory), it's time to evaluate the board state.
    if depth >= maxDepth:
        return [-1, -1, evaluate(state, ourPlayer)]

    # If we haven't hit max depth and victory hasn't been achieved, time to explore deeper.
    if curPlayer == ourPlayer:
        # Best outcome starts out at -inf w.r.t our player
        best = [-1, -1, -Infinity]
        for hex in hexes_by_involvement(state):
            # place piece in hex, then run minimax on the resulting state
            x, y = hex[0], hex[1]
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            score = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer, maxDepth)

            # revert the action, so that a new one can be performed for the next hex
            state.undo_move(move)
            
            # if eval score surpasses the current best, we have a new best move
            score[0], score[1] = x, y
            if score[2] > best[2]:
                best = score

            if ((state.randomLimit - (state.totalTime + (time.process_time() - state.moveStart))) <= 0 ):
                return best

            # if our maximizing player hits a score that is greater than what the minimizing player will consider, break. This board state is now irrelevant and the rest of the possible moves are pruned.
            if best[2] >= (b):
                break
            
            # update alpha so moves further down the minimax tree can use it as a reference
            a = max(a, best[2])
    else:
        # Best outcome starts at inf w.r.t our player
        best = [-1, -1, Infinity]
        for hex in hexes_by_involvement(state):
            x, y = hex[0], hex[1]
            action = ("PLACE", x, y)
            move = state.handle_action(action, _TOKEN_MAP_OUT[curPlayer])
            score = minimax(state, depth + 1, action, a, b, _SWAP_PLAYER[curPlayer], ourPlayer, maxDepth)
            state.undo_move(move)
            score[0], score[1] = x, y
            
            if score[2] < best[2]:
                best = score

            if ((state.randomLimit - (state.totalTime + (time.process_time() - state.moveStart))) <= 0 ):
                return best
            
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

def check_winner(state, action, curPlayer: int, ourPlayer: int) -> int:
    '''
    Checks if victory has been achieved. 
    Returns -1 if loss, 0 if no victory, 1 if victory, w.r.t ourPlayer.
    Code borrowed from game.py in referee module provided by COMP30024 tutors.
    '''
    # We are evaluating victory relative to the player that just played, rather than the player whose turn it is
    prevPlayer = 1 if curPlayer == 2 else 2
    
    # axis is 0 for red, 1 for blue
    axis = 0 if prevPlayer == 1 else 1

    _, r, q = action
    reachable = state.connected_coords((r, q))
    axis_vals = [coord[axis] for coord in reachable]
    # print(f"Checking winner: move = {(r, q)} by player {prevPlayer}")
    # print(f"Axis values = {axis_vals}")
    if min(axis_vals) == 0 and max(axis_vals) == state.n - 1:
        # we have a win for curPlayer! figure out if that's a win for our player or a loss
        return 1 if prevPlayer == ourPlayer else -1
    
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
    return empty_hexes

def hexes_by_involvement(state):
    '''
    Function that returns a list of empty hexes on the board, in descending order of their degree
    '''
    return sorted(empty_hexes(state), key = lambda x: state.hex_degrees[x[0]][x[1]], reverse=True)

def evaluate(state, player: int):
    '''
    Evaluation or utility function. 
    Returns a value for the 'desirability' of a board state based upon an evaluation of certain features.
    '''

    dijkstraScore = dijkstraEvalScore(player, state)
    # avgDistanceScore = -1 * avgDistanceFromCentre(state, player)
    pieceAdvantageScore = pieceAdvantage(state, player)
    opponentEdgeScore = opponentEdge(state, player)
    # triangeStructureScore = triangle_structures(state, player) / 3

    # if shortestPaths[0] > 2 or shortestPaths[1] > 2:
    #     dijkstraScore *= 10
    
    score = (2 * dijkstraScore + pieceAdvantageScore + opponentEdgeScore) 
    # score = dijkstraScore

    # print("EVAL! Action: " + str(action) + ". with respect to player " + str(player) + ". Score = " + str(np.arctan(score)/(np.pi/2)) + ".")
    # print(f"Dijkstra: {dijkstraScore}, Distance: {avgDistanceScore}, Piece Advantage: {pieceAdvantageScore}, Triangle Structure: {triangeStructureScore}")
    # print("State:")
    # print_state(state._data)
    
    # Normalise the score so that it lies in the range [-1, 1]. Note that the extremes are only possible in the case of victory or loss.
    return score

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



