from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

radio_groups = {}

class RadioButton(Widget):
    required_states = ['selected', 'unselected']
    optional_states = ['selected_and_disabled', 'unselected_and_disabled', 
                       'selected_and_focused', 'unselected_and_focused',
                       'selected_and_hovered', 'unselected_and_hovered']

    def __init__(self, parent, name, group=None, selected=False):
        Widget.__init__(self, parent, name)
        self.group = group
        self.selected = selected
        if group:
            key = self.group_key()
            if key not in radio_groups:
                radio_groups[key] = []
            radio_groups[key].append(self)

    def group_key(self):
        # two radio buttons must have the same parent if they are to be
        # in the same radio group
        return "%s/%s" % (str(self.parent), str(self.group))

    def select(self, offset=None):
        if not self.selected:
            self.click(offset)
            
    def click(self, offset=None):
        Widget.click(self, offset)
        self.selected = True
        if not self.group:
            return
        for radio_button in radio_groups[self.group_key()]:
            if radio_button != self:
                radio_button.selected = False