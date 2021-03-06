from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.widgets.table import Table

# TODO: allow lists to forgo having a column header
#
#       Also, it would be ideal if the List could inherit
#       from TableColumn instead of Table. Otherwise, we have
#       an ugly, unnecessary, extra folder lying around.
class List(Table):
    """A list is a special table with just one column"""
    def __init__(self, parent, name, column, 
                 row_height, rows_per_page, pixels_per_scroll=None):
        Table.__init__(self, parent, name, [column], row_height, rows_per_page, pixels_per_scroll)

    def first_row_matching(self, row_value):
        return self.first_row_where(**{self.columns[0].name: row_value})

    def rows_matching(self, row_value):
        return self.rows_where(**{self.columns[0].name: row_value})
