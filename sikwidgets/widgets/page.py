import types
from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.util import to_snakecase

def gen_widget_method(widget_class):
    def widget_method(self, *args, **kwargs):
        return self.create_widget(widget_class, *args, **kwargs)
    return widget_method

class Page(Widget):
    def __init__(self, parent, source_widget, name=None):
        if not name:
            name = to_snakecase(self.__class__.__name__)
        Widget.__init__(self, parent, name)
        # Note: source_widget must have a selected attribute.
        #       eg, a radio button
        self.source_widget = source_widget
        self.widgets = []
        self.add_widget_methods()
        self.contains()

    def exists(self):
        if self.source_widget.selected:
            return True
        return False

    def contains(self):
        pass

    def create_image_folders(self):
        for widget in self.widgets:
            widget.create_image_folder()

    def capture_screenshots(self):
        for widget in self.widgets:
            widget.capture_screenshots()

    def create_widget(self, widget_class, *args, **kwargs):
        widget = widget_class(self, *args, **kwargs)
        self.widgets.append(widget)
        return widget

    def add_widget_methods(self):
        # Page is a special widget that needs to hold other widgets,
        # and sometimes those widgets inherit from Page. To avoid a circular
        # import, let's import all widgets here
        from sikwidgets.widgets import *
        from sikwidgets.widgets import instantiable_widget_class_names
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
