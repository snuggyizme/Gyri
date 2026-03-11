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
    
    def up(self, count):
        """
        Move the cursor up (Y+) in the 2D tape.
        """
        self.y += count

        return self.cells.setdefault((self.x, self.y), 0)
    
    def left(self, count):
        """
        Move the cursor left (X-) in the 2D tape.
        """
        self.x -= count

        return self.cells.setdefault((self.x, self.y), 0)
    
    def down(self, count):
        """
        Move the cursor down (Y-) in the 2D tape.
        """
        self.y -= count

        return self.cells.setdefault((self.x, self.y), 0)
    
    def right(self, count):
        """
        Move the cursor right (X+) in the 2D tape.
        """
        self.x += count

        return self.cells.setdefault((self.x, self.y), 0)