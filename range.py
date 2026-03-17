from tape import Tape
from interpreter import _throw

class Range:
    def __init__(self, head: tuple, tail: tuple, tape: Tape, interpreterIndex: int):
        """
        Creates a custom type called the 'Range'. A range is an ordered group of cell values. It is defined by the <head> and <tail> coordinates.
        Internally, a range is a list of the values of the cells inside the head-tail pair. Ranges can be made in any direction (e.g. @0,0 to @0,5 or @5,0 to @-5,0)
        Ranges cannot be easily stored in a integer/cellvalue and are temporary.
        """
        self.head = head
        self.tail = tail

        self.length = 0

        if self.head == self.tail:
            _throw("Error creating range: head coordinate cannot be the same as tail", interpreterIndex) 
        
        if head[0] == tail[0] and head[1] != tail[1]:
            if head[1] > tail[1]:
                self.indexRanges = (head[0], range(head[1], tail[1] + 1))
            else:
                self.indexRange = (head[0], range(tail[1], head[1] + 1))
        elif head[0] != tail[0] and head[1] == tail[1]:
            if head[0] > tail[0]:
                self.indexRange = (range(head[0], tail[0] + 1), head[1])
            else:
                self.indexRange = (range(tail[0], head[0] + 1), head[1])
        else:
            _throw("Error creating range: range coordinates are not aligned along a dimension", interpreterIndex)
        
        self.values = []

        for x, y in self.indexRange:
            self.values.append(tape.get((x, y)))

    def getAll(self):
        """
        Simply returns the range as a list.
        """
        return self.values
    
    def get(self, index):
        """
        Get the value at <index>
        """
        return self.values[index]