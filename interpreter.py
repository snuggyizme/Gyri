from tape import Tape
TAPE = Tape()
from range import Range

import string
from pathlib import Path
import json

def _throw(error: str, index: int | str):
    raise Exception("GYRI: An error has occurred at character {index} - {error}.")

def _parseNumber(string: str, index: int):
    """
    Read an optional integer starting at <string>[<index>].
    Returns (integer, newIndex)
    """
    set = "0123456789-"
    if index >= len(string) or string[index] not in set:
        return 1, index
    j = index
    while j < len(string) and string[j] in set:
        j += 1
        set = set[0:10]
    return int(string[index:j]), j

def _parseCoordinate(string: str, index: int, __inside__ =  False):
    """
    Reads a coordinate (e.g. @70, 5) starting at <string>[<index>] or a range if the next character is a :
    Returns ((x, y), newIndex, isRange=False) for a coordinate.
    Returns (list[(x, y)], newIndex, isRange=True) for a range.
    """
    if index != "@":
        _throw(f"Error reading coordinate: expected '@', got {string[index]}", index)
    j = index + 1
    x, j = _parseNumber(string, j)
    if x == 1:
        _throw(f"Error reading coordinate: expected an integer as x coordinate", j)
    
    j += 1
    if string[j] != ",":
        _throw(f"Expected ',', got {string[j]}", j)
    y, j = _parseNumber(string, j)
    if y == 1:
        _throw(f"Error reading coordinate: expected an integer as y coordinate", j)

    j += 1
    if string[j] == ":" and not __inside__:
        j += 1
        tail, k, _ = _parseCoordinate(string, j, __inside__ = True)
        return Range((x, y), tail, TAPE, j), j, True
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

def _getArguments(string: str, index: int, expect: list[list[str]], brackets: tuple = ("(", ")")):
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
            if name in TAPE.aliases:
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

def _runtimeData():
    """
    Builds a dict of data + _exe() that is sent to all sets. Contents:

    "exe": _exe
    "pos": ( current pointer position; tuple )
    """

    return {
        "exe": _exe,
        "pos": TAPE.current
    }

def _exe(tag, command, args):
    s = SETS[tag]
    method = getattr(s, command)
    return method(args)

SETS: dict = {}

def _manageArgs(args: tuple | list, expect: list):
    """
    Used to call fuctions from the builtin sets (e.g. p / pointer)

    <args> can be either (string, index) or a list of arguments

    <expect> defines the expected arguements. Each item in <expect> is an arguement and are lists themselves.
    Each item in <expect>[ARGUEMENT] is a string and is a type that is allowed in that arguement.
    """
    if isinstance(input, tuple):
        string, index = args

        args, newIndex = _getArguments(string, index, expect)
        index = newIndex
    
    return args, index

def pset(inp: tuple):
    """
    p:set

    Sets the value at the current pointer position to a given number.

    Arguments must be supplied using _manageArgs()
    Takes [["int"]]
    Returns newIndex
    """
    args, index = inp

    amount = args[0]
    if amount == None:
        _throw("No argument found for command p:set", index if isinstance(index, int) else "Unknown index - outside of script")

    TAPE.set(TAPE.x, TAPE.y, amount)

    return index

def pinc(inp: tuple):
    """
    p:inc

    Increments the value at the current pointer position by a given number.

    Argumenst must be supplied using _manageArgs()
    Takes [["int"]]
    Returns newIndex
    """
    args, index = inp

    amount = args[0]
    if amount == None:
        _throw("No argument found for command p:inc", index if isinstance(index, int) else "Unknown index - outside of script")
    
    TAPE.set(TAPE.x, TAPE.y, TAPE.get((TAPE.x, TAPE.y)) + amount)

def pdec(inp: tuple):
    """
    p:dec

    Decrements the value at the current pointer position by a given number

    Arguments must be supplied using _manageArgs()
    Takes [["int"]]
    Returns newIndex
    """
    args, index = inp

    amount = args[0]
    if amount == None:
        _throw("No argument found for command p:dec", index if isinstance(index, int) else "Unknown index - outside of script")
    
    TAPE.set(TAPE.x, TAPE.y, TAPE.get((TAPE.x, TAPE.y)) - amount)

def pjmp(inp: tuple):
    """
    p:jmp

    I like fly but jmp is normal so :(

    Arguments must be supplied using _manageArgs()

    Returns newIndex
    """
    args, index = inp

    dst = args[0]
    if dst == None:
        _throw("No argument found for command p:jmp", index if isinstance(index, int) else "Unknown index - outside of script")
    
    x, y = (
        dst[0] - TAPE.x,
        dst[1] - TAPE.y,
    )

    if x > 0:
        TAPE.right(x)
    if x < 0:
        TAPE.left(-x)
    
    if y > 0:
        TAPE.up(y)
    if y < 0:
        TAPE.down(-y)

def iprt(inp: tuple):
    """
    i:prt

    Prints the value at a coordinate or the values in a range as their ascii equivalent

    Arguments must be supplied using _manageArgs()
    Takes [["coord", "range"]]
    Returns newIndex
    """
    args, index = inp

    item = args[0]
    if item == None:
        _throw("No argument found for command i:prt", index if isinstance(index, int) else "Unknown index - outside of script")
    elif isinstance(item, list): #  Range case
        for i in item:
            print(chr(i))
    elif isinstance(item, tuple): # Coord case
        print(chr(TAPE.get(item)))
    
    return index

def iprn(inp: tuple):
    """
    i:prn

    Prints the value at a coordinate or the values in a range as their ascii equivalent

    Arguments must be supplied using _manageArgs()
    Takes [["coord", "range"]]
    Returns newIndex
    """
    args, index = inp

    item = args[0]
    if item == None:
        _throw("No argument found for command i:prn", index if isinstance(index, int) else "Unknown index - outside of script")
    elif isinstance(item, list): #  Range case
        for i in item:
            print(item[i])
    elif isinstance(item, tuple): # Coord case
        print(TAPE.get(item))

    return index

def run(code):
    i = 0

    while i < len(code):
        c = code[i]

        match c.lower():

            # Basic movement
            # ======================================================================
            case "w":
                if code[i+1] == ":":
                    break
                count, n = _parseNumber(code, i)
                
                TAPE.up(count)
                i = n if n > i else i + 1

            case "a":
                if code[i+1] == ":":
                    break
                count, n = _parseNumber(code, i)
                
                TAPE.left(count)
                i = n if n > i else i + 1
            
            case "s":
                if code[i+1] == ":":
                    break
                count, n = _parseNumber(code, i)
                
                TAPE.down(count)
                i = n if n > i else i + 1
            
            case "d":
                if code[i+1] == ":":
                    break
                count, n = _parseNumber(code, i)
                
                TAPE.right(count)
                i = n if n > i else i + 1
            # ======================================================================

            # Flight
            # ======================================================================
            case "@":
                combinedCoordinate, newIndex, _ = _parseCoordinate(code, i)

                x, y = combinedCoordinate
                i = newIndex

                if TAPE.x > x:
                    TAPE.left(TAPE.x - x)
                elif TAPE.x < x:
                    TAPE.right(x - TAPE.x)
                
                if TAPE.y > y:
                    TAPE.down(TAPE.y - y)
                elif TAPE.y < y:
                    TAPE.up(y - TAPE.y)
            # ======================================================================

            # Sets
            # ======================================================================
            case "#":
                command, newIndex = _parseName(code, i, "<")
                i = newIndex

                match command:
                    case "include":
                        args, newIndex = _getArguments(code, i, [["str"]], ("<", ">"))
                        i = newIndex
                        
                        if not Path(f"{args[0]}.json").is_file():
                            _throw(f"Could not find set at path {args[0]}", i)

                        with open(f"{args[0]}.json", "r") as file:
                            data = json.load(file)

                        SETS[data["__tag__"]] = data

            # Just like C :P
            # ======================================================================

        # ((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))
        if c in (string.ascii_lowercase + "0123456789") and code[i+1] == ":":
            instruction = code[i+2:i+4]
            i += 5 # We are now at the opening bracket to the arguments

            if c == "p":
                match instruction:
                    case "set":
                        # Arguments:
                        # 1 : int
                        i = pset(_manageArgs((code, i), [["int"]]))                    
                    case "inc":
                        # Arguments:
                        # 1 : int
                        i = pinc(_manageArgs((code, i), [["int"]]))
                    case "jmp":
                        # Arguments:
                        # 1 : coord
                        i = pjmp(_manageArgs((code, i), [["coord"]]))
                    case _:
                        _throw(f"Unknown instruction '{instruction}' in set '{c}'", i)

            elif c == "i":
                match instruction:
                    case "prt":
                        # Arguments:
                        # 1 : coord / range
                        i = iprt(_manageArgs((code, i)))
            elif instruction in SETS[c]:
                pass # imported
            else:
                _throw("Unknown key: make sure you installed and imported the set correctly, and that you are using the correct set key", i) 
                        
                    
        # ((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))