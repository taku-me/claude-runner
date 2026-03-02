from hello import hello, goodbye


def test_hello():
    assert hello("World") == "Hello, World!"


def test_goodbye():
    assert goodbye("World") == "Goodbye, World!"
