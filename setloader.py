import importlib as imp

def load(setName: str):
    module = imp.import_module(setName)
    
    for obj in vars(module).values():
        if isinstance(obj, type) and hasattr(obj, "tag"):
            return obj()
    raise Exception(f"Nothing found while loading set {setName}")
