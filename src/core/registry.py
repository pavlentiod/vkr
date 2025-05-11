

registry = {}

def register(name):
    def wrapper(fn):
        registry[name] = fn
        return fn
    return wrapper

def get(name):
    return registry[name]
