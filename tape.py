from interpreter import _parseCoordinate

class Tape:
    def __init__(self):
        """
        A 2D array of cells.
        The cells are accessed with an X and Y coordinate.
        -X == left, +X == right
        -Y == down, +Y == up
        """
        self.cells = {}
        self.x: int = 0
        self.y: int = 0
        self.aliases = {}
    
    def up(self, count: int):
        """
        Move the cursor up (Y+) in the 2D tape <count> times.
        """
        self.y += count

        self.cells.setdefault((self.x, self.y), 0)
    
    def left(self, count: int):
        """
        Move the cursor left (X-) in the 2D tape <count> times.
        """
        self.x -= count

        self.cells.setdefault((self.x, self.y), 0)
    
    def down(self, count: int):
        """
        Move the cursor down (Y-) in the 2D tape <count> times.
        """
        self.y -= count

        self.cells.setdefault((self.x, self.y), 0)
    
    def right(self, count: int):
        """
        Move the cursor right (X+) in the 2D tape <count> times.
        """
        self.x += count

        self.cells.setdefault((self.x, self.y), 0)
    
    def get(self, coordinates: tuple):
        """
        Get the value of the cell <coordinates>
        """
        self.cells.setdefault(coordinates, 0)
        return self.cells[coordinates]
    
    def set(self, x: int, y: int, value: int):
        """
        Set the value at (<x>, <y>) to <value>
        """
        self.cells[(x, y)] = value

    def current(self):
        """
        Returns the current x and y positions
        """
        return (self.x, self.y)
    
    def inc(self, coordinates: tuple, count: int):
        """
        Increments the value at <coordinates> by <count>
        """
        self.cells.setdefault(coordinates, 0)
        self.cells[coordinates] += count
    
    def dec(self, coordinates: tuple, count: int):
        """
        Decrements the value at <coordinates> by <count>
        """
        self.cells.setdefault(coordinates, 0)
        self.cells[coordinates] -= count
    
    def makeAlias(self, name: str, coordinate: tuple):
        """
        Creates a name that is replaced with its assigned (x, y) coordinate automatically.
        """
        self.aliases[name] = coordinate
    
    def resolve(self, string: str):
        """
        Takes in a <string> that is either an alias or a coordinate and returns it as a coordinate
        """
        if string in self.aliases:
            return self.aliases[string]
        return _parseCoordinate(string, 0)[0]