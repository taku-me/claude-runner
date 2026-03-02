def hello(name):
    return f"Hello, {name}!"


def goodbye(name):
    return f"Goodbye, {name}!"


def greet_all(names):
    return [hello(name) for name in names]
