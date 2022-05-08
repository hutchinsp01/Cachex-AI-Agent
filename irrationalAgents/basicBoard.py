"""
Provide a class to maintain the state of a Cachex game board, including
some helper methods to assist in updating and searching the board.

Code borrowed from 'referee' package written for COMP30024 Project B at The University of Melbourne
"""

from queue import Queue
from numpy import zeros, array, roll, vectorize
from collections import defaultdict as dd

# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)], 
    dtype="i,i")

# Pre-compute diamond capture patterns - each capture pattern is a 
# list of offset steps:
# [opposite offset, neighbour 1 offset, neighbour 2 offset]
#
# Note that the "opposite cell" offset is actually the sum of
# the two neighbouring cell offsets (for a given diamond formation)
#
# Formed diamond patterns are either "longways", in which case the
# neighbours are adjacent to each other (roll 1), OR "sideways", in
# which case the neighbours are spaced apart (roll 2). This means
# for a given cell, it is part of 6 + 6 possible diamonds.
_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2] 
    for n1, n2 in 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) + 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]

# Maps between player string and internal token type
_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

# Map between player token types
_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

class Board:
    def __init__(self, n, board = None):
        """
        Initialise board of given size n.
        """
        self.n = n
        
        if board is None:
            self._data = zeros((n, n), dtype=int)
        else:
            self._data = board

        # set start and end edges for the colours
        self.blue_start = [(i, 0) for i in range(n)]
        self.blue_end = [(i, n-1) for i in range(n)]
        self.red_start = [(j, i) for (i, j) in self.blue_start]
        self.red_end = [(j, i) for (i, j) in self.blue_end]

        # initialise number of turns taken.
        self.turns_taken = 0

        # initialise list of occupied hexes
        # self.occupied_hexes = []

        #initialise array of hex degrees
        self.hex_degrees = zeros((n, n), dtype=int)

    def __getitem__(self, coord):
        """
        Get the token at given board coord (r, q).
        """
        return _TOKEN_MAP_OUT[self._data[coord]]

    def __setitem__(self, coord, token):
        """
        Set the token at given board coord (r, q).
        """
        self._data[coord] = _TOKEN_MAP_IN[token]

    def digest(self):
        """
        Digest of the board state (to help with counting repeated states).
        Could use a hash function, but not really necessary for our purposes.
        """
        return self._data.tobytes()

    def swap(self):
        """
        Swap player positions by mirroring the state along the major 
        board axis. This is really just a "matrix transpose" op combined
        with a swap between player token types.
        """
        self.turns_taken += 1
        swap_player_tokens = vectorize(lambda t: _SWAP_PLAYER[t])
        self._data = swap_player_tokens(self._data.transpose())
        
        # update hex degrees - inefficient but should only happen once :)
        for i in range(self.n):
            for j in range(self.n):
                 if self._data[i][j] != 0:
                     self.change_neighbour_degrees((i,j), 1)
                     self.change_neighbour_degrees((j,i), -1)

    def change_neighbour_degrees(self, coord: tuple, amount: int):
        for neighbour in self._coord_neighbours(coord):
            self.hex_degrees[neighbour[0]][neighbour[1]] += amount

    
    def place(self, token, coord):
        """
        Place a token on the board and apply captures if they exist.
        Return coordinates of captured tokens.
        """
        self.turns_taken += 1
        self[coord] = token
        self.change_neighbour_degrees((coord), 1)
        return self._apply_captures(coord)

    def connected_coords(self, start_coord):
        """
        Find connected coordinates from start_coord. This uses the token 
        value of the start_coord cell to determine which other cells are
        connected (e.g., all will be the same value).
        """
        # Get search token type
        token_type = self._data[start_coord]

        # Use bfs from start coordinate
        reachable = set()
        queue = Queue(0)
        queue.put(start_coord)

        while not queue.empty():
            curr_coord = queue.get()
            reachable.add(curr_coord)
            for coord in self._coord_neighbours(curr_coord):
                if coord not in reachable and self._data[coord] == token_type:
                    queue.put(coord)

        return list(reachable)

    def inside_bounds(self, coord):
        """
        True iff coord inside board bounds.
        """
        r, q = coord
        return r >= 0 and r < self.n and q >= 0 and q < self.n

    def is_occupied(self, coord):
        """
        True iff coord is occupied by a token (e.g., not None).
        """
        return self[coord] != None

    def _apply_captures(self, coord):
        """
        Check coord for diamond captures, and apply these to the board
        if they exist. Returns a list of captured token coordinates.
        """
        opp_type = self._data[coord]
        mid_type = _SWAP_PLAYER[opp_type]
        captured = set()

        # Check each capture pattern intersecting with coord
        for pattern in _CAPTURE_PATTERNS:
            coords = [_ADD(coord, s) for s in pattern]
            # No point checking if any coord is outside the board!
            if all(map(self.inside_bounds, coords)):
                tokens = [self._data[coord] for coord in coords]
                if tokens == [opp_type, mid_type, mid_type]:
                    # Capturing has to be deferred in case of overlaps
                    # Both mid cell tokens should be captured
                    captured.update(coords[1:])

        # Remove any captured tokens
        for coord in captured:
            self[coord] = None
            self.change_neighbour_degrees(coord, -1)

        return list(captured)

    def _coord_neighbours(self, coord):
        """
        Returns (within-bounds) neighbouring coordinates for given coord.
        """
        return [_ADD(coord, step) for step in _HEX_STEPS \
            if self.inside_bounds(_ADD(coord, step))]

    def handle_action(self, action, player):
        captured = None

        actionType, *args = action
        if actionType == "STEAL":
            # Apply STEAL action
            self.swap()
            return "STEAL"

        elif actionType == "PLACE":

            coord = tuple(args)
            captured = self.place(player, coord)
            return (player, coord, captured)

    def undo_move(self, move):
        
        if move == None:
            return
        elif move == "STEAL":
            self.swap()
            # cancel out turn count increase
            self.turns_taken -= 1
        else:
            self._data[move[1][0], move[1][1]] = 0
            self.change_neighbour_degrees((move[1][0], move[1][1]), -1)
            opponent = _SWAP_PLAYER[_TOKEN_MAP_IN[move[0]]]
            for captured in move[2]:
                self._data[captured[0]][captured[1]] = opponent
                self.change_neighbour_degrees((captured[0], captured[1]), 1)

        # decrement turn count
        self.turns_taken -= 1

