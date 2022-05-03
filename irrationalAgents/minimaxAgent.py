from numpy import Infinity
from irrationalAgents.helpers.minimax import minimax
from irrationalAgents.basicBoard import _TOKEN_MAP_IN, Board
import copy

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
        self.playerInt = _TOKEN_MAP_IN[self.player]
        self.board = Board(n)


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        position = minimax(self.board, 0, None, -Infinity, +Infinity, self.playerInt, self.playerInt)
        return ("PLACE", position[0], position[1]) 


    
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
        self.board.handle_action(action, player)


