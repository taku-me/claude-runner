VERSION = "1.0.0"

import logging

logger = logging.getLogger(__name__)


def hello(name):
    logger.debug("hello called with name=%r", name)
    if not name:
        name = "World"
    return f"Hello, {name}!"


def goodbye(name):
    logger.debug("goodbye called with name=%r", name)
    if not name:
        name = "World"
    return f"Goodbye, {name}!"


def greet_all(names):
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]
