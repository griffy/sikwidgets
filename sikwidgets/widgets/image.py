from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError

class Image(Widget):
    required_states = ['enabled']
    optional_states = ['disabled', 'hovered']
    