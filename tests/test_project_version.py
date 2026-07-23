from app.config_manager import ConfigManager

config = ConfigManager()

print("=" * 40)

print("Project 1 URL:")
print(config.project_url("Project 1"))

print()

print("Project 1 Version:")
print(config.project_version("Project 1"))

print("=" * 40)