from range import Range

def _throw(error: str, index: int | str):
    raise Exception(f"GYRI: An error has occurred at character {index} - {error}.")

def _parseNumber(string: str, index: int):
    """
    Read an optional integer starting at <string>[<index>].
    Returns (integer, newIndex)
    """
    nums = "0123456789-"
    if index >= len(string) or string[index] not in nums:
        return None, index
    j = index
    while j < len(string) and string[j] in nums:
        j += 1
        nums = nums[0:10]
    return int(string[index:j]), j

def _parseCoordinate(string: str, index: int, tape, __inside__ =  False):
    """
    Reads a coordinate (e.g. @70, 5) starting at <string>[<index>] or a range if the next character is a :
    Returns ((x, y), newIndex, isRange=False) for a coordinate.
    Returns (list[(x, y)], newIndex, isRange=True) for a range.
    """
    if string[index] != "@":
        _throw(f"Error reading coordinate: expected '@', got {string[index]}", index)
    j = index + 1
    x, j = _parseNumber(string, j)
    if x == 1:
        _throw(f"Error reading coordinate: expected an integer as x coordinate", j)
    
    if string[j] != ",":
        _throw(f"Expected ',', got {string[j]}", j)
    y, j = _parseNumber(string, j)
    if y == 1:
        _throw(f"Error reading coordinate: expected an integer as y coordinate", j)

    if string[j] == ":" and not __inside__:
        j += 1
        tail, k, _ = _parseCoordinate(string, j, __inside__ = True)
        return Range((x, y), tail, tape, j), j, True
    return (x, y), j, False

def _parseName(string: str, index: int, stopper: str):
    """
    Reads <string>[<index>] up until the first <stopper>.
    <stopper> must be one character.
    Returns (name, newIndex)
    """
    export = ""
    
    while string[index] != stopper:
        export += string[index]
        index += 1
    return export, index

def _getArguments(string: str, index: int, expect: list[list[str]], tape, brackets: tuple = ("(", ")")):
    """
    Reads an optional list of arguments for an instruction, starting at <string>[<index>].
    The arguements should be in parenthesis and seperated by commas.
    Returns (arguements[], newIndex), or (None, newIndex) if no arguements are found.

    <expect> defines the expected arguements. Each item in <expect> is an arguement and are lists themselves.
    Each item in <expect>[ARGUEMENT] is a string and is a type that is allowed in that arguement. Types supported in this function:
    "int": integer
    "coord": coordinate on 2D tape.
    "range": range of coordiantes on 2D tape.

    <brackets> is an optional argument that changes what is detected for the start and end of the arguments.
    """
    export = []
    argType = []

    if string[index] != brackets[0]:
        return None, index
    j = index + 1

    argNum = 0
    inside = True
    while j < len(string) and inside:
        if string[j] == ")":
            inside = False
            j += 1
            break
            break

        if argNum > len(expect):
            _throw(f"Too many arguments", j)
        
        if string[j] in "0123456789":
            argType = ["int"]
        elif string[j] == "@":
            argType = ["coord", "range"]
        else:
            name, j = _parseName(string, j, ",")
            if name in tape.aliases:
                pass
            else:
                _throw("Unknown arguement type: expected coordinate, alias, range or integer", j)
        
        if not any(item in expect[argNum] for item in argType):
            match argType:
                case ["int"]:
                    argTypeDisplay = "int"
                case ["coord", "range"]:
                    argTypeDisplay = "coordinate or range"
                case _:
                    argTypeDisplay = "unknown type"
            _throw(f"Wrong argument, expected {expect[argNum]}, got {argTypeDisplay}", j)
        
        if argType == ["int"]:
            value, j = _parseNumber(string, j)
            export.append(value)
        elif argType == ["coord", "range"]:
            value, j, _ = _parseCoordinate(string, j)
            export.append(value)
        
        argNum += 1

        if string[j] == ",":
            j += 1
        elif string[j] == brackets[1]:
            inside = False
            j += 1
        else:
            _throw(f"Expected ',' or '{brackets[1]}' after argument", j)
    
    return export, j