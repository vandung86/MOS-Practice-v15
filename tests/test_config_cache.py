from app.config_manager import ConfigManager

config = ConfigManager()

print("Lần 1")
config.load()

print("Lần 2")
config.load()

print("Lần 3")
config.load()