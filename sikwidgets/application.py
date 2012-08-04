import time

from sikuli.Sikuli import App

class Application:
    open_cmd = ""
    windows = []

    def __init__(self):
        if not self.open_cmd:
            # TODO: look for ___icon___/ under images/,
            # construct a button, and click it when open is called
            pass
        self.app = App(self.open_cmd)
        self.window_instances = [None for window in self.windows]

    # FIXME: rename / rewrite this method?
    def init_window(self, window_class):
        return window_class(self.app.focusedWindow())

    def create_image_folders(self):
        # temporarily instantiate all the windows with the same
        # focused window region (which is -wrong-, but it doesn't
        # matter in this case) to create their image folders all at once
        for window_class in self.windows:
            self.init_window(window_class).create_image_folders()

    def capture_screenshots(self):
        self.create_image_folders()
        # temporarily instantiate all the windows with the same
        # focused window region (which is -wrong-, but it doesn't
        # matter in this case) 
        for window_class in self.windows:
            self.init_window(window_class).capture_screenshots()

    def open(self):
        self.app.open()

    def find_focused_window(self):
        for i, window_class in enumerate(self.windows):
            window = window_class(self.app.focusedWindow())
            if window.exists():
                self.window_instances[i] = window
                return window
        return None

    def focused_window(self, wait=5):
        time.sleep(wait)
        window = self.find_focused_window()
        return window