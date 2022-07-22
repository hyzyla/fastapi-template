"""
Thin wrapper around Sentry SDK, to hide details and do not depend on one product
"""
import logging
from contextlib import contextmanager
from typing import Any, Iterator

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

Scope = sentry_sdk.Scope


def init(dsn: str | None, environment: str) -> None:
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        shutdown_timeout=10,
        integrations=[
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.ERROR,  # Send errors as events
            ),
        ],
    )


def capture_exception(error: BaseException) -> None:
    sentry_sdk.capture_exception(error=error)


def set_attachment(key: str, value: bytes) -> None:
    """
    Add large value to sentry context
    """
    return sentry_sdk.Hub.current.scope.add_attachment(
        bytes=value,
        filename=key,
    )


def set_context(key: str, value: Any) -> None:
    """
    Add large value to sentry context
    """
    return sentry_sdk.set_context(
        key=key,
        value=value,
    )


@contextmanager
def configure_scope() -> Iterator[Scope]:
    with sentry_sdk.configure_scope() as scope:

        yield scope

        scope.clear()
