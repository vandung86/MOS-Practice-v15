from app.update_manager import UpdateManager

update = UpdateManager()

path = update.download_project(
    "Project 1"
)

print(path)