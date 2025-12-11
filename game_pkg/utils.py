def log_transaction(func):
    def wrapper(*args, **kwargs):
        print(f"[SYSTEM LOG] Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper