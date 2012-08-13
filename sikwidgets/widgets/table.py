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
                # return the row's index in the current page and the row itself
                yield (page_row_index, self.rows[current_row_index])
                current_row_index += 1
            # we scanned the full page of visible rows
            scanned_page = True
            if not self.scrollbar_at_bottom():
                # but there are more pages to scan
                if settings.DEBUG:
                    print "Reached end of rows; scrolling down a page"
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

    # TODO: in the process of converting this to a generator
    #       method first_row_where and rows_where will call
    def next_row_where(self, **kwargs):
        row_scanner = self.row_scanner()
        page_row_index, row = row_scanner.next()
        while row:
            for column_name, cell_value in kwargs.iteritems():
                if not row.column_has(column_name, cell_value):
                    # one of the column values didn't match,
                    # so this row isn't a match
                    break

            row = row_scanner.next()

                    cell_region = self.cell_region_at(cur_cell)
                    # hover over it as visual feedback
                    cell_region.hover(cell_region)
                    # look within the cell region for cell value
                    match = None
                    if use_text:
                        # search for the text in the cell region
                        match = self.do_find_in(cell_region, cell_value)
                    else:
                        # search within the cell region to find the expected cell
                        # (checking all its states)
                        match = self.expected_cell[cell_value].find_in(cell_region)

                    if match:
                        if settings.DEBUG:
                            print "Found a cell matching '%s'" % cell_value
                        row_index = cur_cell + total_rows_scrolled
                        yield TableCell(self, match, row_index)




        row_cells = {}
        for column_name, cell_value in kwargs.iteritems():
            matching_cells = self.column[column_name].cells_with(cell_value)
            if not matching_cells:
                yield None
            elif row_cells is None:
                row_cells = {}
                for cell in matching_cells:
                    row_cells[cell.row_index] = [cell]
            else:
                for row_index, cells in row_cells.iteritems():
                    cell = filter(lambda c: c.row_index == row_index, matching_cells)
                    if not cell:
                        del row_cells[row_index]
                    else:
                        row_cells[row_index].append(cell[0])
        rows = []
        for row_index, cells in row_cells.iteritems():
            rows.append(TableRow(self, row_index, cells))
        return rows

    def cell_exists(self, column_name, cell_value):
        if self.first_cell_where(**{column_name: cell_value}):
            return True
        return False

    # FIXME: make more efficient (short-circuit)
    #        Use a generator like in TableColumn
    def first_row_where(self, **kwargs):
        rows = self.rows_where(**kwargs)[0]
        if rows:
            return rows[0]
        return None


    def rows_where(self, **kwargs):
        # TODO: improve search algorithm so that only the rows
        #       that match so far are searched within for the
        #       desired column value instead of the entire table
        #       per column

        row_cells = None
        for column_name, cell_value in kwargs.iteritems():
            if row_cells and len(row_cells) <= 0:
                break

            matching_cells = self.column[column_name].cells_with(cell_value)
            if not matching_cells:
                return []
            elif row_cells is None:
                row_cells = {}
                for cell in matching_cells:
                    row_cells[cell.row_index] = [cell]
            else:
                for row_index, cells in row_cells.iteritems():
                    cell = filter(lambda c: c.row_index == row_index, matching_cells)
                    if not cell:
                        del row_cells[row_index]
                    else:
                        row_cells[row_index].append(cell[0])
        rows = []
        for row_index, cells in row_cells.iteritems():
            rows.append(TableRow(self, row_index, cells))
        return rows

    def first_cell_where(self, column_name, cell_value):
        return self.column[column_name].first_cell_with(cell_value)

    def cells_where(self, column_name, cell_value):
        return self.column[column_name].cells_with(cell_value)
            
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

    def first_cell_with(self, cell_value):
        # TODO: check cache
        return self.next_cell_with(cell_value).next()
        # TODO: store cell in cache
 
    def cells_with(self, cell_value):
        # TODO: check cache
        cells = []
        cell_gen = self.next_cell_with(cell_value)
        cell = cell_gen.next()
        while cell:
            cells.append(cell)
            cell = cell_gen.next()
        # TODO: store cells in cache
        return cells



    # TODO: scrolling left or right to show columns :|
    #       It should be done like this:
    #           scroll_left until desired_column.exists()
    # FIXME: this needs rewritten / broken up into separate functions
    def next_cell_with(self, cell_value):
        # TODO: should use_text be a named parameter the user passes?
        use_text = False
        if cell_value not in self.expected_cell:
            use_text = True

        self.table.scroll_to_top()
        self.locate_header()

        total_rows_scrolled = 0
        starting_cell = 0
        scanned_page = False
        while not self.table.scrollbar_at_bottom() or not scanned_page:
            for cur_cell in range(starting_cell, self.table.rows_per_page):
                cell_region = self.cell_region_at(cur_cell)
                # hover over it as visual feedback
                cell_region.hover(cell_region)
                # look within the cell region for cell value
                match = None
                if use_text:
                    # search for the text in the cell region
                    match = self.do_find_in(cell_region, cell_value)
                else:
                    # search within the cell region to find the expected cell
                    # (checking all its states)
                    match = self.expected_cell[cell_value].find_in(cell_region)

                if match:
                    if settings.DEBUG:
                        print "Found a cell matching '%s'" % cell_value
                    row_index = cur_cell + total_rows_scrolled
                    yield TableCell(self, match, row_index)
            scanned_page = True
            if not self.table.scrollbar_at_bottom():
                if settings.DEBUG:
                    print "Reached end of page, scrolling down one"
                rows_scrolled = self.table.scroll_down(self.table.rows_per_page)
                total_rows_scrolled += rows_scrolled
                starting_cell = self.table.rows_per_page - rows_scrolled
                scanned_page = False
        yield None

# As we search in TableColumn or TableRow and a cell doesn't already exist,
# *create* one with the column and row_index. THEN use its methods to find
# itself.

class TableCell(Widget):
    """ A generated, "virtual" widget. Its region is actually a Match from
        a search performed in TableColumn.
    """
    def __init__(self, table, column, row):
        Widget.__init__(self, table)
        self.table = table
        self.column = column
        self.row = row
        self.search_region = self.cell
        self.column = column
        self.table = column.table
        self.row = row

    def cell_region_at(row_index):
        """ Returns the region which will be searched in
            for the cell at the given row index in the table
        """
        self.locate_header()
        # find the cell's index on the current page of the table
        page_cell_index = row_index % self.table.rows_per_page
        y_offset = self.table.row_height + (page_cell_index * self.table.row_height)
        cell_region = self.header_region.offset(Location(0, y_offset))
        cell_region.setH(self.table.row_height)
        cell_region = cell_region.nearby(self.table.row_height / 2)
        return cell_region

    # TODO: need to scroll right (if necessary) as well
    def scroll_to(self):
        self.table.scroll_to_left()
        self.table.scroll_to_top()
        num_scrolls_down = max(self.row_index+1 - self.table.rows_per_page, 0)
        self.table.scroll_down(num_scrolls_down)
        if self.num_scrolls_right is None:
            while self.column.exists(force_check=True)
        self.table.scroll_right(self.num_scrolls_right)

    # FIXME: the methods below are too naive. They will not work
    #        if the page has been scrolled. A cell needs to know
    #        how many clicks from the top (or left) it is when
    #        it is discovered
    # def hover(self, offset=None, force_check=False): pass

    # def click(self, offset=None, force_check=False): pass

    # def double_click(self, offset=None, force_check=False): pass

    # def right_click(self, offset=None, force_check=False): pass


class TableRow(Widget):
    """ A generated, "virtual" widget """

    def __init__(self, table, index, scrolls_from_top):
        Widget.__init__(self, table)
        self.table = table
        self.index = index
        self.scrolls_from_top = scrolls_from_top
        self.cell = {}

    def contains(column_name, cell_value):
        region_contains

    def cell_under(self, column_name):
        # if we already had the cell stored, return it
        cell = filter(lambda c: c.column.name == column_name, self.cells)
        if cell:
            return cell[0]
        # otherwise, search for it
        self.scroll_to()
        column = self.table.column[column_name]
        return column.cell_region_at()

    def scroll_to(self):
        self.table.scroll_to_top()
        num_scrolls = max(self.index+1 - self.table.rows_per_page, 0)
        self.table.scroll_down(num_scrolls)

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
