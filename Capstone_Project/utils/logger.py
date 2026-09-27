"""Centralized logger factory for the framework."""
from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_LOGGERS: dict[str, logging.Logger] = {}
_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Return an idempotent logger with console + rotating file handlers."""
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        import sys; console = logging.StreamHandler(stream=sys.stdout.reconfigure(encoding="utf-8", errors="replace") if hasattr(sys.stdout, "reconfigure") else sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(console)

        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(
            log_dir / "framework.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(fh)

    _LOGGERS[name] = logger
    return logger
