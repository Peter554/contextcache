import asyncio
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


def test_disallow_nested_caching() -> None:
    with pytest.raises(contextcache.NestedCaching):
        with contextcache.use_caching(double):
            with contextcache.use_caching(double, allow_nested=False):
                ...


_async_double_cache = contextvars.ContextVar("async_double_cache", default=None)


@contextcache.async_enable_caching(_async_double_cache)
async def async_double(i: int) -> int:
    logging.warning(f"calling double with {i}")
    await asyncio.sleep(0.1)  # working...
    return i * 2


@pytest.mark.asyncio
async def test_async_caching(caplog: pytest.LogCaptureFixture) -> None:
    assert (await async_double(1)) == 2
    assert (await async_double(1)) == 2
    assert caplog.messages == ["calling double with 1", "calling double with 1"]
    caplog.clear()

    with contextcache.use_caching(async_double):
        assert (await async_double(1)) == 2
        assert (await async_double(1)) == 2
    assert caplog.messages == ["calling double with 1"]
    caplog.clear()

    with contextcache.use_caching(async_double):
        await asyncio.gather(*[async_double(1) for _ in range(10)])
        # Will use the cache
        await asyncio.gather(*[async_double(1) for _ in range(10)])
    assert caplog.messages == ["calling double with 1"] * 10
    caplog.clear()

    async def _task() -> int:
        with contextcache.use_caching(async_double):
            return await async_double(1)

    await asyncio.gather(*[_task() for _ in range(10)])
    await asyncio.gather(*[_task() for _ in range(10)])
    assert caplog.messages == ["calling double with 1"] * 20
    caplog.clear()
