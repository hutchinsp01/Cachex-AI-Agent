import numpy as np
from basicBoard import Board
from queue import PriorityQueue
from dijkstraTile import dijkstraTile
import sys, json

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
            board = handle_input(data)
            (cost, path) = getDijkstraDistance(2, board)
            print("Cost = " + str(cost))
            print("Path = ")
            print(path)

    except IndexError:
        print("usage: python3 evaluation.py path/to/input.json", file=sys.stderr)
        sys.exit(1)
    
    return

def handle_input(file):
    size = file["n"]
    start = (file["start"][0], file["start"][1])
    goal = (file["goal"][0], file["goal"][1])
    
    board = np.zeros((size, size), dtype=int)
    conversion = {"b" : 2, "r" : 1}
    
    for tile in file["board"]:
        board[tile[1]][tile[2]] = conversion[tile[0]]

    return Board(size, board)


def getDijkstraDistance(color: int, board: Board = None) -> tuple:
    '''
    Function is applied to a board state. Returns the number of hexes
    needed to complete the shortest path between edges of the board for 
    a particular colour (1 = red, 2 = blue).
    '''
    
    # Set starting edge. We check shortest path from all tiles on this edge to the opposite edge.
    edge = board.blue_start if color == 2 else board.red_start

    shortestPaths = [dijkstraPath(tile, color, board) for tile in edge]
    
    # go through all shortest paths from start edge to end edge and return the path cost,
    # and path tiles, of said path
    min = np.inf
    shortestPath = []
    for (cost, path) in shortestPaths:
        if cost < min:
            min = cost
            shortestPath = path
    
    return (min, shortestPath)

def dijkstraPath(tile: tuple, color: int, board: Board) -> tuple:
    '''
    Returns the number of hexes needed to complete the shortest path from a particular starting tile
    to an edge, as well as the coords of all tiles on that path
    '''
    
    # figure out our destination
    destinationEdge = board.blue_end if color == 2 else board.red_end

    # all tiles on the board whose path lengths (from start tile) have been found by Dijkstra. All start as False.
    lockedIn = np.zeros((len(board._data), len(board._data)), dtype=bool)
    
    # we haven't found a path yet. Let's initialise our priority queue to be used in Dijkstra's algorithm.
    
    found = False
    queue = PriorityQueue()
    (i, j) = tile

    if board._data[i][j] == color:
        queue.put(dijkstraTile(tile, 0))
    elif board._data[i][j] == 0:
        queue.put(dijkstraTile(tile, 1))
    else:
        # opposing color occupies start tile; no path possible
        return -1
    
    # perform dijkstra's algo over whole board until the closest destination tile is reached
    while queue.qsize() > 0:
        print("Queue size: " + str(queue.qsize()))
        tile = queue.get()
        cost = tile.cost
        
        print("Expanding: " + str(tile.coords))
       
        # check if we have hit a destination tile
        if tile.coords in destinationEdge:
            print("Hit!")
            # lock in the destination tile, then create a list of the tiles on the path to it
            lockedIn[tile.coords[0]][tile.coords[1]] = True
            path = []
            pathNode = tile
            while pathNode:
                path.insert(0, pathNode.coords)
                pathNode = pathNode.parent
            
            return (tile.cost, path)
        
        # if this tile already has a locked-in cost value, we ignore it and move on
        if lockedIn[tile.coords[0]][tile.coords[1]]:
            continue
        
        lockedIn[tile.coords[0]][tile.coords[1]] = True
        for neighbour in board._coord_neighbours(tile.coords):
            print(neighbour)
            (i, j) = neighbour

            if board._data[i][j] == color:
                queue.put(dijkstraTile(neighbour, cost, tile))
            elif board._data[i][j] == 0:
                queue.put(dijkstraTile(neighbour, cost + 1, tile))
            else:
                continue
    
    return (-1, None)

main()