from sikwidgets.application import Application

from windows.tasks import Tasks

class TaskManager(Application):
    open_cmd = "C:\\Windows\\System32\\taskmgr.exe"
    windows = [Tasks]
        