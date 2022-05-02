from irrationalAgents.basicBoard import _SWAP_PLAYER

def pieceAdvantage(state, player):
    playerCount = 0
    opponentCount = 0

    opponent = _SWAP_PLAYER[player]

    for i in range (0, len(state._data)):
            for j in range(0, len(state._data)):
                if state._data[i][j] == player:
                    playerCount += 1
                if state._data[i][j] == opponent:
                    opponentCount += 1

    return playerCount - opponentCount