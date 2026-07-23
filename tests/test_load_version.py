from app.cache import CacheManager

cache = CacheManager()

version = cache.load_version(
    "Project 1"
)

print(version)