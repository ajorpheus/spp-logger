import getpass
import json
import logging
import sys
from datetime import datetime
from typing import IO
from uuid import uuid4

import immutables
import pytz as pytz

from .config import SPPLoggerConfig


class SPPHandler(logging.StreamHandler):
    def __init__(
        self,
        config: SPPLoggerConfig,
        context: immutables.Map = None,
        log_level: int = logging.INFO,
        stream: IO = sys.stdout,
    ) -> None:
        self.config = config
        super().__init__(stream=stream)
        if context is None:
            context = immutables.Map(
                log_correlation_id=str(uuid4()),
                log_level=log_level,
            )
        self._context = self.set_context(context)
        self.level = self._context.get("log_level")

    def format(self, record: logging.LogRecord) -> str:
        log_message = {
            "log_level": record.levelname,
            "timestamp": self.get_timestamp(record),
            "description": record.getMessage(),
            "service": self.config.service,
            "component": self.config.component,
            "environment": self.config.environment,
            "deployment": self.config.deployment,
            "user": self.get_user(),
        }
        return json.dumps(
            {
                **log_message,
                **{k: self.context[k] for k in self.context if k not in ["log_level"]},
                "log_level_conf": logging.getLevelName(self.level),
            }
        )

    def get_timestamp(self, record: logging.LogRecord) -> str:
        tz = pytz.timezone(self.config.timezone)
        return datetime.fromtimestamp(record.created, tz).isoformat()

    def get_user(self) -> str:
        if self.config.user is None:
            self.config.user = getpass.getuser()
        return self.config.user

    def set_context_attribute(self, attribute_name: str, attribute_value: str) -> None:
        if attribute_name in self._context:
            raise ImmutableContextError.attribute_error(attribute_name)
        self._context = self.context.set(attribute_name, attribute_value)

    @property
    def context(self) -> immutables.Map:
        return self._context

    def set_context(self, context: immutables.Map) -> immutables.Map:
        if type(context) is not immutables.Map:
            raise ImmutableContextError("Context must be a type of 'immutables.Map'")
        self._context = context
        self.level = self.context.get("log_level")
        return self.context


class ImmutableContextError(Exception):
    pass

    @classmethod
    def attribute_error(cls, attribute_name: str) -> "ImmutableContextError":
        return cls(
            "Context attributes are immutable, could not override "
            + f"'{attribute_name}'"
        )


class ContextError(Exception):
    pass
