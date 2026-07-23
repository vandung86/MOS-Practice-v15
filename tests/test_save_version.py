from app.cache import CacheManager

cache = CacheManager()

cache.save_version(
    "Project 1",
    "1.0"
)

print("Save OK")