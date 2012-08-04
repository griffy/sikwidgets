from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

class Button(Widget):
    required_states = ['enabled']
    optional_states = ['disabled', 'focused', 'hovered']
