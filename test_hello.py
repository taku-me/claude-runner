from hello import hello, goodbye, greet_all


def test_hello():
    assert hello("World") == "Hello, World!"


def test_goodbye():
    assert goodbye("World") == "Goodbye, World!"


def test_greet_all():
    assert greet_all(["Alice", "Bob"]) == ["Hello, Alice!", "Hello, Bob!"]


def test_greet_all_empty():
    assert greet_all([]) == []
