VERSION = "1.0.0"

import logging

logger = logging.getLogger(__name__)


def _greet(greeting, name):
    logger.debug("%s called with name=%r", greeting.lower(), name)
    if not name:
        name = "World"
    logger.info("%s, %s!", greeting, name)
    return f"{greeting}, {name}!"


def hello(name):
    return _greet("Hello", name)


def goodbye(name):
    return _greet("Goodbye", name)


def greet_all(names):
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]
