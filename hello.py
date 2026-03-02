VERSION = "1.0.0"

import logging

logger = logging.getLogger(__name__)


def hello(name):
    logger.debug("hello called with name=%r", name)
    if name is None or name == "":
        name = "World"
    logger.info("Hello, %s!", name)
    return f"Hello, {name}!"


def goodbye(name):
    logger.debug("goodbye called with name=%r", name)
    if name is None or name == "":
        name = "World"
    logger.info("Goodbye, %s!", name)
    return f"Goodbye, {name}!"


def greet_all(names):
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]
