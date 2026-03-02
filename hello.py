VERSION = "1.0.0"
AUTHOR = "claude-runner"

import logging

logger = logging.getLogger(__name__)


def hello(name):
    logger.debug("hello called with name=%r", name)
    if name is None or name == "":
        name = "World"
    return f"Hello, {name}!"


def goodbye(name):
    logger.debug("goodbye called with name=%r", name)
    if name is None or name == "":
        name = "World"
    return f"Goodbye, {name}!"


def greet_all(names):
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]


def count_greetings(names):
    logger.debug("count_greetings called with %d name(s)", len(names))
    greetings = greet_all(names)
    logger.info("Greeted %d person(s)", len(greetings))
    return len(greetings)
