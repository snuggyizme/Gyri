class Remote:
    def __init__(self):
        self.tag = "r"
        self.display = "Remote"

    def inc(self, runtimeData: dict, destination: tuple, value: int):
        self.rtd = runtimeData
        source = self.rtd["pos"]

    
    