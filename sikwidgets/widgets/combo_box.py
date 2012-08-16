from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.widgets.list import List

# TODO: add more state to be aware of when list/dropdown is visible
class ComboBox(List):
    def __init__(self, parent, name, 
                 row_height, rows_per_page, pixels_per_scroll=None):
    	List.__init__(self, parent, name, "__selected__",
    				  row_height, rows_per_page, pixels_per_scroll)

    def hover(self, offset=None, force_check=False):
        self.column().hover(offset, force_check)

    def click(self, offset=None, force_check=False):
        self.column().click(offset, force_check)