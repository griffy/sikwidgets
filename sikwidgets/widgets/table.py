import os

from sikuli.Sikuli import Location

from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.widgets.button import Button
from sikwidgets.widgets.scrollable_widget import ScrollableWidget
from sikwidgets import settings
from sikwidgets.util import clicks_per_widget

# TODO: create subfolders of table columns for each expected cell.
#       This way, cells can have states just like other widgets.
#       Also, it keeps things cleaner.
# 
#       binary searching
#
#       know how far left/down to click

# TableRow and TableCell instances should be created on-demand,
# and each should be able to find itself and do all the functions
# of a regular widget. So, they need regions (a row is the sum of its
# child cell regions).
# When they are created, they should be accessible to the Table
# and the appropriate TableColumns so that they are not lost
# between operations.

# TODO:
# TableColumn should probably cache rows and cells that it
# finds.
class Table(ScrollableWidget):
    def __init__(self, parent, name, columns, 
                 row_height, rows_per_page, pixels_per_scroll=None):
        ScrollableWidget.__init__(self, parent, name)
        self.set_columns(columns)
        self.rows = []
        self.set_row_attributes(row_height, rows_per_page, pixels_per_scroll)

    def set_row_attributes(row_height, rows_per_page, pixels_per_scroll=None):
        self.row_height = row_height
        self.rows_per_page = rows_per_page
        if not pixels_per_scroll:
            # the sane default per scroll is exactly one row
            self.pixels_per_scroll = row_height
        self.clicks_per_row = clicks_per_widget(self.row_height, self.pixels_per_scroll)

    def add_column(self, column_name):
        column = TableColumn(self, column_name)
        # keep an ordered list so we know how the columns go
        # left-to-right
        self.columns.append(column)
        # keep a hash so we can conveniently access columns by name
        self.column[column_name] = column

    def set_columns(self, column_names):
        self.columns = []
        self.column = {}
        for column_name in column_names:
            self.add_column(column_name)

    def capture_screenshots(self):
        for column in self.columns:
            column.capture_screenshots()
        # capture screenshots of the scrollbars
        ScrollableWidget.capture_screenshots(self)

    def scroll_up(self, num_rows=1):
        num_clicks = num_rows * self.clicks_per_row
        actual_clicks = ScrollableWidget.scroll_up(self, num_clicks)
        actual_rows = actual_clicks / self.clicks_per_row
        return actual_rows

    def scroll_down(self, num_rows=1):
        num_clicks = num_rows * self.clicks_per_row
        actual_clicks = ScrollableWidget.scroll_down(self, num_clicks)
        actual_rows = actual_clicks / self.clicks_per_row
        return actual_rows

    def row_scanner(self):
        self.scroll_to_top()
        # the index of a row in terms of the visible page
        starting_page_row_index = 0
        # the amount of times we've scrolled in terms of rows
        total_rows_scrolled = 0
        current_row_index = 0
        scanned_page = False
        while not self.scrollbar_at_bottom() or not scanned_page:
            # loop through the visible page of rows
            for page_row_index in range(starting_page_row_index, self.rows_per_page):
                if len(self.rows) <= current_row_index:
                    # If the row hasn't been generated yet, do so.
                    # The row needs to know its index in the overall table
                    # as well as the amount of scrolls necessary to reach it
                    # from the top
                    self.rows.append(TableRow(self, current_row_index, total_rows_scrolled))
                yield self.rows[current_row_index]
                current_row_index += 1
            # we scanned the full page of visible rows
            scanned_page = True
            if not self.scrollbar_at_bottom():
                # but there are more pages to scan
                if settings.DEBUG:
                    print "Reached end of row page; scrolling down a page"
                rows_scrolled = self.scroll_down(self.rows_per_page)
                if not rows_scrolled:
                    break
                total_rows_scrolled += rows_scrolled
                starting_page_row_index = self.rows_per_page - rows_scrolled
                scanned_page = False
        yield None

    def first_row_where(self, **kwargs):
        return self.next_row_where(**kwargs).next()

    def rows_where(self, **kwargs):
        rows = []
        row_gen = self.next_row_where(**kwargs)
        row = row_gen.next()
        while row:
            rows.append(row)
            row = row_gen.next()
        return rows

    def next_row_where(self, **kwargs):
        row_scanner = self.row_scanner()
        row = row_scanner.next()
        while row:
            match = True
            for column_name, cell_value in kwargs.iteritems():
                if not row.cell_exists(column_name, cell_value, force_scroll=False):
                    # one of the column values didn't match,
                    # so this row isn't a match
                    match = False
                    break
            if match:
                yield row
            row = row_scanner.next()
        yield None

    def cell_exists(self, column_name, cell_value):
        if self.first_cell_where(column_name, cell_value):
            return True
        return False

    def first_cell_where(self, column_name, cell_value):
        return self.column[column_name].first_cell_matching(cell_value)

    def cells_where(self, column_name, cell_value):
        return self.column[column_name].cells_matching(cell_value)
            
    def exists(self, force_check=False):
        for column in self.columns:
            if column.exists(force_check):
                return True
        return False


class TableColumn(Widget): 
    def __init__(self, table, name):
        Widget.__init__(self, table, name)
        self.table = table
        # create a button for the column header
        # FIXME: It is assumed that all tables have headers in
        #        order to function correctly.
        self.header = Button(self, "__header__")
        self.header_region = None
        self.scrolls_from_left = None
        self.load_expected_cells()

    def load_expected_cells(self):
        self.expected_cell = {}
        path = self.image_folder()
        expected_cells = [cell for cell in os.listdir(path) if os.path.isdir(os.path.join(path, cell))]
        for cell_name in expected_cells:
            self.expected_cell[cell_name] = Widget(self, cell_name)

    def exists(self, force_check=False):
        if self.locate_header(force_check):
            return True
        return False

    def hover(self, offset=None, force_check=False):
        self.header.hover(offset, force_check)

    def click(self, offset=None, force_check=False):
        """ Alias so user doesn't have to say .header.click each time """
        self.header.click(offset, force_check)

    def double_click(self, offset=None, force_check=False):
        self.header.double_click(offset, force_check)

    def right_click(self, offset=None, force_check=False):
        self.header.right_click(offset, force_check)

    def drag_to(self, x, y, force_check=False):
        self.header.drag_to(x, y, force_check)

    def drag_onto(self, widget, force_check=False):
        self.header.drag_onto(widget, force_check)

    def locate_header(self, force_check=False):
        header = self.header.find(force_check)
        if header:
            if settings.DEBUG:
                print "Found column '%s'" % self.name
            self.header_region = header
        else:
            self.header_region = None
        return header

    def scroll_to(self):
        self.table.scroll_to_left()
        if self.scrolls_from_left is None:
            self.scrolls_from_left = 0
            while not self.exists(force_check=True):
                self.table.scroll_right()
                self.scrolls_from_left += 1
        else:
            self.table.scroll_right(self.scrolls_from_left)

    def cell_in(self, row):
        return TableCell(self.table, self, row, self.expected_cell)

    def has_cell_matching_in(self, row, cell_value, force_scroll=True):
        if self.cell_matching_in(row, cell_value, force_scroll):
            return True
        return False

    # FIXME: rewrite this method so that it lets the TableCell check
    #        itself
    def cell_matching_in(self, row, cell_value, force_scroll=True):
        if self.cell_in(row).matches(cell_value, force_column_scroll=force_scroll):
            return cell
        return None

    def first_cell_matching(self, cell_value, force_scroll=True):
        return self.next_cell_matching(cell_value, force_scroll).next()
 
    def cells_matching(self, cell_value, force_scroll=True):
        cells = []
        cell_gen = self.next_cell_matching(cell_value, force_scroll)
        cell = cell_gen.next()
        while cell:
            cells.append(cell)
            cell = cell_gen.next()
        return cells

    def next_cell_matching(self, cell_value, force_scroll=True):
        if force_scroll:
            self.scroll_to()

        row_scanner = self.table.row_scanner()
        row = row_scanner.next()
        while row:
            cell = self.cell_matching_in(row, cell_value, force_scroll=False)
            if cell:
                yield cell
            row = row_scanner.next()
        yield None


class TableRow(Widget):
    """ A generated, "virtual" widget """

    def __init__(self, table, index, scrolls_from_top):
        Widget.__init__(self, table)
        self.table = table
        self.index = index
        if index < self.table.rows_per_page:
            self.page_index = index
        else:
            self.page_index = self.table.rows_per_page - 1
        self.scrolls_from_top = scrolls_from_top

    def cell_exists(column_name, cell_value, force_scroll=True):
        if force_scroll:
            self.scroll_to()
        return self.table.column[column_name].has_cell_matching_in(self, cell_value)

    def cell_under(self, column_name):
        return self.table.column[column_name].cell_in(self)

    def scroll_to(self):
        self.table.scroll_to_top()
        self.table.scroll_down(self.scrolls_from_top)

    def hover(self, offset=None, force_check=False):
        self.cells[0].hover(offset, force_check)

    def click(self, offset=None, force_check=False):
        """ Alias so user doesn't have to say .cells[0].click each time """
        self.cells[0].click(offset, force_check)

    def double_click(self, offset=None, force_check=False):
        self.cells[0].double_click(offset, force_check)

    def right_click(self, offset=None, force_check=False):
        self.cells[0].right_click(offset, force_check)

    def drag_to(self, x, y, force_check=False):
        self.cells[0].drag_to(x, y, force_check)

    def drag_onto(self, widget, force_check=False):
        self.cells[0].drag_onto(widget, force_check)


# TODO: add search methods and region generation
#       should be able to scroll to and find itself


class TableCell(Widget):
    """ A generated, "virtual" widget. Its region is actually a Match from
        a search performed in TableColumn.
    """
    def __init__(self, table, column, row, expected_cell_map):
        Widget.__init__(self, table)
        self.table = table
        self.column = column
        self.row = row
        self.expected_cell = expected_cell_map
        self.find_search_region()

    def matches(self, cell_value, force_column_scroll=True, force_row_scroll=True):
        if force_column_scroll:
            self.column.scroll_to()
        if force_row_scroll:
            self.row.scroll_to()

        if cell_value in self.expected_cell:
            if self.expected_cell[cell_value].exists_in(self.search_region):
                return True
        elif self == cell_value:
            return True
        return False

    def find_search_region(self):
        """ Find the region which will be searched in
            for the cell in the table
        """
        header = self.column.locate_header()
        y_offset = self.table.row_height + (self.row.page_index * self.table.row_height)
        cell_region = header.offset(Location(0, y_offset))
        cell_region.setH(self.table.row_height)
        self.search_region = cell_region.nearby(self.table.row_height / 2)

    def scroll_to(self):
        self.column.scroll_to()
        self.row.scroll_to()

    def hover(self, offset=None, force_check=False):
        self.scroll_to()
        Widget.hover(self, offset, force_check)

    def click(self, offset=None, force_check=False):
        self.scroll_to()
        Widget.click(self, offset, force_check)

    def double_click(self, offset=None, force_check=False):
        self.scroll_to()
        Widget.double_click(self, offset, force_check)

    def right_click(self, offset=None, force_check=False):
        self.scroll_to()
        Widget.right_click(self, offset, force_check)

    def drag_to(self, x, y, force_check=False):
        self.scroll_to()
        Widget.drag_to(x, y, force_check)

    def drag_onto(self, widget, force_check=False):
        if (isinstance(widget, TableCell) or 
            isinstance(widget, TableRow) or
            isinstance(widget, TableColumn):
            # these widgets must be scrolled to first so they're
            # visible
            widget.scroll_to()
        self.scroll_to()
        Widget.drag_onto(widget, force_check)

