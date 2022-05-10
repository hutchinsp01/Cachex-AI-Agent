from irrationalAgents1.basicBoard import Board

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

        for i in range (0,self.board.n):
            for j in range(0, self.board.n):
                if self.player == "blue":
                    if self.board._data[i][j] == 0:
                        return ("PLACE", i, j)
                
                if self.player == "red":
                    if self.board._data[j][i] == 0:
                        return ("PLACE", j, i)


    
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

