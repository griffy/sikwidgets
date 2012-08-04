from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

class CheckBox(Widget):
    required_states = ['checked', 'unchecked']
    optional_states = ['checked_and_disabled', 'unchecked_and_disabled', 
                       'checked_and_focused', 'unchecked_and_focused',
                       'checked_and_hovered', 'unchecked_and_hovered']
 
    def check(self, offset=None):
        if self.is_checked() or self.is_checked_and_focused():
            return

        self.click(offset)

    def uncheck(self, offset=None):
        if self.is_unchecked() or self.is_unchecked_and_focused():
            return

        self.click(offset)