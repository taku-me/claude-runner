from hello import hello, goodbye, hello_all


def test_hello():
    assert hello("World") == "Hello, World!"


def test_goodbye():
    assert goodbye("World") == "Goodbye, World!"


def test_hello_all():
    assert hello_all(["Alice", "Bob"]) == ["Hello, Alice!", "Hello, Bob!"]


def test_hello_all_empty():
    assert hello_all([]) == []


def test_hello_empty_string():
    assert hello("") == "Hello, World!"


def test_hello_none():
    assert hello(None) == "Hello, World!"


def test_goodbye_empty_string():
    assert goodbye("") == "Goodbye, World!"


def test_goodbye_none():
    assert goodbye(None) == "Goodbye, World!"
