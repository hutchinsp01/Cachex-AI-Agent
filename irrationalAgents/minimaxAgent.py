from numpy import Infinity
from irrationalAgents.constants import DEPTH1, DEPTH2, DEPTH3, DEPTH4
from irrationalAgents.helpers.minimax import empty_hexes, minimax
from irrationalAgents.helpers.pieces import opponentEdge
from irrationalAgents.basicBoard import _TOKEN_MAP_IN, Board
import time

class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.playerColour = player
        self.player = _TOKEN_MAP_IN[self.playerColour]
        self.board = Board(n)


    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        self.board.moveStart = time.process_time()

        if ((self.board.randomLimit - (self.board.totalTime + (time.process_time() - self.board.moveStart))) <= 0 ):
            position = empty_hexes(self.board)[0]
        elif self.board.turns_taken == 0:
            position = (0,0)
        elif self.board.turns_taken == 1:
            return ("STEAL", )
        else:
            numHexes = self.board.n * self.board.n - len(self.board.occupied_hexes)

            maxDepth = 5
            if numHexes > DEPTH4:
                maxDepth = 4
            if numHexes > DEPTH3:
                maxDepth = 3
            if numHexes > DEPTH2:
                maxDepth = 2
            if numHexes > DEPTH1:
                maxDepth = 1


            position = minimax(self.board, 0, None, -Infinity, +Infinity, self.player, self.player, maxDepth)

        self.board.totalTime = self.board.totalTime + (time.process_time() - self.board.moveStart)

        print(f"{self.player} {opponentEdge(self.board, self.playerColour)}")

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


