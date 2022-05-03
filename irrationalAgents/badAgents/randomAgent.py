from irrationalAgents.basicBoard import Board
from numpy import random

class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.player = player
        self.board = Board(n)


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        n = len(self.board._data)
        r = random.randint(n)
        q = random.randint(n)

        while (self.board._data[r][q] != 0):
            r = random.randint(n)
            q = random.randint(n)
        
        return ("PLACE", r, q)



    
    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """

        actionType, *args = action
        if actionType == "STEAL":
            # Apply STEAL action
            self.board.swap()

        elif actionType == "PLACE":
            coord = tuple(args)
            self.board.place(player, coord)