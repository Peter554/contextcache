import contextvars

import contextcache

# Define a private ContextVar to store the cached values. Don't touch this ContextVar!
_double_cache = contextvars.ContextVar("double_cache", default=None)


# Use the `enable_caching` decorator to enable context caching for `double`.
@contextcache.enable_caching(_double_cache)
def double(n: int) -> int:
    print(f"doubling {n}")
    return n * 2


# Without caching.
print(double(1))
print(double(1))

# With caching.
with contextcache.use_caching(double):
    print(double(2))
    print(double(2))
