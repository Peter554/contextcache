import logging
import contextvars

import pytest

import contextcache

_double_cache = contextvars.ContextVar("double_cache", default=None)


@contextcache.enable_caching(_double_cache)
def double(i: int) -> int:
    logging.warning(f"calling double with {i}")
    return i * 2


def test_caching(caplog: pytest.LogCaptureFixture) -> None:
    assert double(1) == 2
    assert double(1) == 2
    assert caplog.messages == ["calling double with 1", "calling double with 1"]
    caplog.clear()

    with contextcache.use_caching(double):
        assert double(1) == 2
        assert double(1) == 2
    assert caplog.messages == ["calling double with 1"]
    caplog.clear()

    assert double(1) == 2
    assert double(1) == 2
    assert caplog.messages == ["calling double with 1", "calling double with 1"]
    caplog.clear()
