VERSION = "1.0.0"

import logging

logger = logging.getLogger(__name__)


def hello(name: str) -> str:
    logger.debug("hello called with name=%r", name)
    if not name:
        name = "World"
    logger.info("Hello, %s!", name)
    return f"Hello, {name}!"


def goodbye(name: str) -> str:
    logger.debug("goodbye called with name=%r", name)
    if not name:
        name = "World"
    logger.info("Goodbye, %s!", name)
    return f"Goodbye, {name}!"


def greet_all(names: list[str]) -> list[str]:
    logger.debug("greet_all called with %d name(s)", len(names))
    return [hello(name) for name in names]
