import types
from sikwidgets.region_group import RegionGroup
from sikwidgets.util import to_snakecase
from sikwidgets.widgets import *

def gen_widget_method(widget_class):
    def widget(self, *args, **kwargs):
        return self.create_widget(widget_class, *args, **kwargs)
    return widget

class Window(RegionGroup):
    def __init__(self, region, parent=None):
        # FIXME: this is hacky
        RegionGroup.__init__(self, parent)
        # manually set the region to the given one rather
        # than the region from the parent
        self.search_region = region
        self.region = region
        self.widgets = []
        self.windows = []
        self.add_widget_methods()
        self.contains()

    # FIXME: str() shouldn't return a URI.. use image_folder() method for this
    def __str__(self):
        uri = to_snakecase(self.__class__.__name__)
        if self.parent:
            uri = os.path.join(str(self.parent), uri)
        return uri

    def create_image_folders(self):
        for widget in self.widgets:
            widget.create_image_folder()
        for window in self.windows:
            window.create_image_folders()

    def capture_screenshots(self):
        for widget in self.widgets:
            widget.capture_screenshots()
        for window in self.windows:
            window.capture_screenshots()

    def contains(self):
        pass
        
    # TODO: use some basic statistics to decide
    #       if we see the window or not
    def exists(self):
        #pop_size = len(self.widgets)
        #n = sample_size(pop_size)
        #random.sample(self.widgets, n)

        seen_widgets = 0
        unseen_widgets = 0
        for widget in self.widgets:
            if widget.exists():
                seen_widgets += 1
            else:
                unseen_widgets += 1
            if seen_widgets > 2 * unseen_widgets + 1:
                return True
        if seen_widgets >= unseen_widgets:
            return True
        return False

    def create_widget(self, widget_class, *args, **kwargs):
        widget = widget_class(self, *args, **kwargs)
        self.widgets.append(widget)
        return widget

    def add_widget_methods(self):
        for class_name in instantiable_widget_class_names:
            widget_class = eval(class_name)
            method = types.MethodType(gen_widget_method(widget_class), self, self.__class__)
            # take the class, get its name in string form, and convert to snake case
            method_name = to_snakecase(widget_class.__name__)
            setattr(self, method_name, method)

    def menu(self, menu_class, *args, **kwargs):
        return self.create_widget(menu_class, *args, **kwargs)

    def page(self, page_class, *args, **kwargs):
        return self.create_widget(page_class, *args, **kwargs)

    def window(self, window_class):
        # since the region for a child window may actually be larger than
        # the region for this window, we should default to passing the 
        # entire screen
        window = window_class(self.region.getScreen(), self)
        self.windows.append(window)
        return window
