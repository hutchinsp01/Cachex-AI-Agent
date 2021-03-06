import numpy as np
from irrationalAgents.basicBoard import Board
from queue import PriorityQueue
from irrationalAgents.helpers.dijkstraTile import dijkstraTile
import sys, json

# def main():
#     try:
#         with open(sys.argv[1]) as file:
#             data = json.load(file)
#             board = handle_input(data)
#             print(board._data)
#             print("Evaluation score for blue: " + str(dijkstraEvalScore(2, board)))

#     except IndexError:
#         print("usage: python3 evaluation.py path/to/input.json", file=sys.stderr)
#         sys.exit(1)
    
#     return

# def handle_input(file):
#     size = file["n"]
#     start = (file["start"][0], file["start"][1])
#     goal = (file["goal"][0], file["goal"][1])
    
#     board = np.zeros((size, size), dtype=int)
#     conversion = {"b" : 2, "r" : 1}
    
#     for tile in file["board"]:
#         board[tile[1]][tile[2]] = conversion[tile[0]]

#     return Board(size, board)

def dijkstraEvalScore(playerColor: int, board: Board) -> int:
    '''
    Returns eval score based on difference between shortest path completion for opposition and shortest path completion for player
    '''
    # print("Player color = " + str(playerColor))
    oppositionColor = 1 if playerColor == 2 else 2
    n = board.n
    # ourDistance = None
    # opponentDistance = None

    ourDistance = getDijkstraDistance(playerColor, board)
    opponentDistance = getDijkstraDistance(oppositionColor, board)

    # if ourDistance == None and opponentDistance == None:
    #     return 0

    # if ourDistance == None and opponentDistance != None:
    #     return opponentDistance

    # if ourDistance == 0:
    #     return np.inf
    
    # if ourDistance != None and opponentDistance == None:
    #     try:
    #         return 1/ourDistance
    #     except:
    #         return np.inf
    
    # else:
    return opponentDistance - ourDistance

    

def getDijkstraDistance(color: int, board: Board) -> int:
    '''
    Returns the number of hexes needed to complete the shortest path from a particular starting tile
    to an edge, as well as the coords of all tiles on that path
    '''

    startEdge = board.blue_start if color == 2 else board.red_start
    
    # figure out our destination
    destinationEdge = board.blue_end if color == 2 else board.red_end

    # all tiles on the board whose path lengths (from start tile) have been found by Dijkstra. All start as False.
    size = len(board._data)
    lockedIn = np.zeros((size, size), dtype=bool)

    # all tile costs are infinite until they are discovered
    tileCosts = np.full((size,size), np.inf)
    
    # we haven't found a path yet. Let's initialise our priority queue to be used in Dijkstra's algorithm.
    
    found = False
    queue = PriorityQueue()

    for tile in startEdge:
        (i, j) = tile

        if board._data[i][j] == color:
            queueCost = 0
        elif board._data[i][j] == 0:
            queueCost = 1
        else:
            # opposing color occupies start tile; no path possible
            continue
        
        queue.put(dijkstraTile(tile, queueCost))
        tileCosts[i][j] = queueCost

    # perform dijkstra's algo over whole board until the closest destination tile is reached
    while queue.qsize() > 0:
        tile = queue.get()
        expandCost = tile.cost

        # check if we have hit a destination tile
        if tile.coords in destinationEdge:
            # lock in the destination tile, then create a list of the tiles on the path to it
            lockedIn[tile.coords[0]][tile.coords[1]] = True
            path = []
            pathNode = tile
            while pathNode:
                path.insert(0, pathNode.coords)
                pathNode = pathNode.parent
            
            # return (tile.cost, path)
            return tile.cost
        
        # if this tile already has a locked-in cost value, we ignore it and move on
        if lockedIn[tile.coords[0]][tile.coords[1]]:
            continue
        
        lockedIn[tile.coords[0]][tile.coords[1]] = True
        for neighbour in board._coord_neighbours(tile.coords):
            (i, j) = neighbour

            if board._data[i][j] == color:
                queueCost = expandCost
            elif board._data[i][j] == 0:
                queueCost = expandCost + 1
            else:
                continue

            # if tile costs less than its current estimate, add it to the priority queue and update its cost in the tileCosts array
            if queueCost < tileCosts[i][j]:
                queue.put(dijkstraTile(neighbour, queueCost, tile))
                tileCosts[i][j] = queueCost
    
    # return (np.inf, None)
    return np.inf