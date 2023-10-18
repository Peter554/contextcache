import contextvars

import contextcache

# Define a private ContextVar to store the cached values. Don't touch this ContextVar!
# You need to define a separate ContextVar for every function for which you want to enable caching.
# contextcache can't do this for you since ContextVars must be global. Use `None` as the default.
_double_cache = contextvars.ContextVar("double_cache", default=None)


# Use the `enable_caching` decorator to enable context caching for `double`.
@contextcache.enable_caching(_double_cache)
def double(n: int) -> int:
    print(f"Doubling {n}, working...")
    return n * 2


# Without caching.
print(f"Without caching")
print(double(1))
print(double(1))

# With caching.
with contextcache.use_caching(double):
    print(f"\nWith caching")
    print(double(1))
    print(double(1))

# Without caching, again.
print(f"\nWithout caching, again")
print(double(1))
print(double(1))
