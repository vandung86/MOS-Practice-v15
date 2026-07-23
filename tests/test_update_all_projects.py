from app.update_manager import UpdateManager
from app.logger_manager import LoggerManager
from app.config import BASE_DIR

logger = LoggerManager(BASE_DIR)

update = UpdateManager(logger)

update.update_all_projects()