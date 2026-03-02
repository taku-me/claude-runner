from hello import hello, goodbye, greet_all, goodbye_all


def test_hello():
    assert hello("World") == "Hello, World!"


def test_goodbye():
    assert goodbye("World") == "Goodbye, World!"


def test_greet_all():
    assert greet_all(["Alice", "Bob"]) == ["Hello, Alice!", "Hello, Bob!"]


def test_greet_all_empty():
    assert greet_all([]) == []


def test_hello_empty_string():
    assert hello("") == "Hello, World!"


def test_hello_none():
    assert hello(None) == "Hello, World!"


def test_goodbye_empty_string():
    assert goodbye("") == "Goodbye, World!"


def test_goodbye_none():
    assert goodbye(None) == "Goodbye, World!"


def test_goodbye_all():
    assert goodbye_all(["Alice", "Bob"]) == ["Goodbye, Alice!", "Goodbye, Bob!"]


def test_goodbye_all_empty():
    assert goodbye_all([]) == []
