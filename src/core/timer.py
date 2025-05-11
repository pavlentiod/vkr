import time

def timed(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {fn.__name__} took {end - start:.4f}s")
        return result
    return wrapper
