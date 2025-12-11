# game_pkg/utils.py

def log_transaction(func):
    """
    Decorator that logs the function name to the console.
    """
    def wrapper(*args, **kwargs):
        # args[0] is 'self', useful for debugging
        print(f"[SYSTEM LOG] Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper