class Remote:
    def __init__(self, execute):
        self.tag = "r"
        self.display = "Remote"

        self.exe = execute

        self.contents = {
            "commands": [
                "inc", "dec", "set", "get", "add", "sub", "mul", "fdv", "cdv", "hlp"
            ] # [   ]  [   ]  [   ]  [   ]  [   ]  [   ]  [   ]  [   ]  [   ]  [   ]
        }

    def inc(self, runtimeData: dict, destination: tuple, value: int):
        self.rtd = runtimeData
        source = self.rtd["pos"]
        self.exe("p", "jmp", destination)
        self.exe("p", "inc", value)
        self.exe("p", "jmp", source)