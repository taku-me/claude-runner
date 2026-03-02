from hello import hello, goodbye, greet_all


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


def test_hello_no_args():
    assert hello() == "Hello, World!"


def test_goodbye_no_args():
    assert goodbye() == "Goodbye, World!"
