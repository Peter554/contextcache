import contextcache

# Define a private CacheContextVar to store the cached values. Don't touch this CacheContextVar from anywhere else!
# You need to define a separate CacheContextVar for every function for which you want to enable caching.
# Use `None` as the default.
_double_cache = contextcache.CacheContextVar("double_cache", default=None)


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
