import sys
from loguru import logger as _logger


def get_logger(name: str):
    _logger.remove()
    _logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - {message}",
        level="INFO",
    )
    return _logger.bind(name=name)


def chunk_list(lst: list, size: int) -> list[list]:
    """Split a list into fixed-size chunks."""
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def flatten(nested: list[list]) -> list:
    return [item for sublist in nested for item in sublist]
