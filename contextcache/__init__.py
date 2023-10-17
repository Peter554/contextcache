import contextvars
import contextlib
from typing import TypeVar, ParamSpec, Callable, Any, cast, Generator, Awaitable


class ContextVarAlreadyAssignedToCache(Exception):
    ...


_registry: dict[Callable[..., Any], contextvars.ContextVar[Any]] = {}


P = ParamSpec("P")
T = TypeVar("T")


def enable_caching(
    contextvar: contextvars.ContextVar[Any],
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    if contextvar in set(_registry.values()):
        raise ContextVarAlreadyAssignedToCache

    def decorator(f: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = (*args, *[(k, v) for k, v in kwargs.items()])
            cache = contextvar.get()
            if cache is not None and cache_key in cache:
                return cast(T, cache[cache_key])
            result = f(*args, **kwargs)
            if cache is not None:
                cache[cache_key] = result
            return result

        _registry[wrapper] = contextvar
        return wrapper

    return decorator


def async_enable_caching(
    contextvar: contextvars.ContextVar[Any],
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    if contextvar in set(_registry.values()):
        raise ContextVarAlreadyAssignedToCache

    def decorator(f: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = (*args, *[(k, v) for k, v in kwargs.items()])
            cache = contextvar.get()
            if cache is not None and cache_key in cache:
                return cast(T, cache[cache_key])
            result = await f(*args, **kwargs)
            if cache is not None:
                cache[cache_key] = result
            return result

        _registry[wrapper] = contextvar
        return wrapper

    return decorator


@contextlib.contextmanager
def use_caching(f: Callable[..., Any]) -> Generator[None, None, None]:
    contextvar = _registry[f]
    if contextvar.get() is not None:
        yield
        return
    contextvar.set({})
    try:
        yield
    finally:
        contextvar.set(None)