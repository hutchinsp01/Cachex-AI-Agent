from functools import total_ordering

@total_ordering
class dijkstraTile:
    '''
    Represents a tile that is being explored as part of Dijkstra's algorithm
    '''
    def __init__(self, tileCoords: tuple, cost: int, parent = None):
        self.coords = tileCoords
        self.parent = parent
        self.cost = cost
    
    def __gt__(self, other):
        return self.cost > other.cost
    
    def __eq__(self, other):
        return self.cost == other.cost
    
