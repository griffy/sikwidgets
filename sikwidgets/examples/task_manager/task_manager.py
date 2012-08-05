from sikwidgets.application import Application
from windows.task_manager_window import TaskManagerWindow

class TaskManager(Application):
    open_cmd = "C:\\Windows\\System32\\taskmgr.exe"
    windows = [TaskManagerWindow]
        