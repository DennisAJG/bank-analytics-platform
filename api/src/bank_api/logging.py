from __future__ import annotations

import logging
import sys

import structlog

DEFAULT_LOG_FORMAT = "%(message)s"

def configure_logging(log_level: str = "INFO") -> None:
    
    logging.basicConfig(
        format=DEFAULT_LOG_FORMAT,
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
def get_logger(name: str = "bank_api"):
    return structlog.get_logger(name)