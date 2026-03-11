from tape import Tape

def parseNumber(string, index):
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

def run(code):
    TAPE = Tape()
    i = 0

    while i < len(code):
        c = code[i]

        match c.lower():

            # Basic movement
            # ======================================================================
            case "w":
                count, n = parseNumber(code, i)
                
                TAPE.up(count)
                i = n

            case "a":
                count, n = parseNumber(code, i)

                TAPE.left(count)
                i = n
            
            case "s":
                count, n = parseNumber(code, i)
                
                TAPE.down(count)
                i = n
            
            case "d":
                count, n = parseNumber(code, i)
                
                TAPE.right(count)
                i = n
            # ======================================================================

            # Flight
            # ======================================================================
            case "@":
                x, n = parseNumber(code, i)

                i = n + 1 # Skip over the comma

                y, n = parseNumber(code, i)

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