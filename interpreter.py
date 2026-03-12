from tape import Tape

def _throw(error: str, index: int):
    raise Exception("GYRI: An error has occurred at character {index} - {error}.")

def _parseNumber(string, index):
    """
    Read an optional integer starting at <string>[<index>].
    Returns (integer, newIndex)
    """
    if index >= len(string) or string[index] not in "0123456789":
        return 1, index
    j = index
    while j < len(string) and string[j] in "0123456789":
        j += 1
    return int(string[index:j]), j

def _getArguments(string, index):
    """
    Reads an optional list of arguements for an instruction, starting at <string>[<index>].
    The arguements should be in parenthesis and seperated by commas.
    Returns (arguements[], newIndex)
    """
    if string[index] != "(":
        return ([], index)
    j = index
    inside = True
    while j < len(string) and inside:
        if string[j] == ")":
            inside = False

def _parseCoordinate(string, index):
    """
    Reads a coordinate (e.g. @70, 5) starting at <string>[<index>].
    Returns ((x, y), newIndex)
    """
    if index !=

def run(code):
    TAPE = Tape()
    i = 0

    while i < len(code):
        c = code[i]

        match c.lower():

            # Basic movement
            # ======================================================================
            case "w":
                count, n = _parseNumber(code, i)
                
                TAPE.up(count)
                i = n

            case "a":
                count, n = _parseNumber(code, i)

                TAPE.left(count)
                i = n
            
            case "s":
                count, n = _parseNumber(code, i)
                
                TAPE.down(count)
                i = n
            
            case "d":
                count, n = _parseNumber(code, i)
                
                TAPE.right(count)
                i = n
            # ======================================================================

            # Flight
            # ======================================================================
            case "@":
                x, n = _parseNumber(code, i)

                i = n + 1 # Skip over the comma

                y, n = _parseNumber(code, i)

                i = n

                if TAPE.x > x:
                    TAPE.left(TAPE.x - x)
                elif TAPE.x < x:
                    TAPE.right(x - TAPE.x)
                
                if TAPE.y > y:
                    TAPE.down(TAPE.y - y)
                elif TAPE.y < y:
                    TAPE.up(y - TAPE.y)
            # ======================================================================

            # ((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))
            case ":":
                instruction = code[i+1:i+3]

                match instruction:
                    
                    # Basic modification of integers
                    # --------------------------------------------------------------
                    case "set":
                        """
                        wait gah i dont want to code this its 1234 o clcok
                        """
                        startPosition = "gah"
            # ((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))