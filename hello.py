VERSION = "1.0.0"

__all__ = ["VERSION", "hello", "goodbye", "greet_all"]

import logging

logger = logging.getLogger(__name__)


def hello(name):
    logger.debug("hello called with name=%r", name)
    if not name:
        name = "World"
    logger.info("Hello, %s!", name)
    return f"Hello, {name}!"


def goodbye(name):
    logger.debug("goodbye called with name=%r", name)
    if not name:
        name = "World"
    logger.info("Goodbye, %s!", name)
    return f"Goodbye, {name}!"


def greet_all(names):
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]
