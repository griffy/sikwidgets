from sikwidgets.application import Application
from windows.task_manager_window import TaskManagerWindow

from sikwidgets import settings
settings.IMAGES_PATH = "images-winxp-default"

class TaskManager(Application):
    open_cmd = "C:\\Windows\\System32\\taskmgr.exe"
    windows = [TaskManagerWindow]
        