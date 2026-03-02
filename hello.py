def hello(name):
    if not name:
        name = "World"
    return f"Hello, {name}!"


def goodbye(name):
    if not name:
        name = "World"
    return f"Goodbye, {name}!"


def greet_all(names):
    return [hello(name) for name in names]
