from sikuli.Sikuli import Location

from sikwidgets.widgets.widget import Widget
from sikwidgets.widgets.widget import WidgetError
from sikwidgets.widgets.button import Button
from sikwidgets.widgets.scrollable_widget import ScrollableWidget
from sikwidgets import settings

# TODO: create subfolders of table columns for each expected cell.
#       This way, cells can have states just like other widgets.
#       Also, it keeps things cleaner.
# 
#       binary searching
#
#       know how far left/down to click

# TODO:
# TableColumn should probably cache rows and cells that it
# finds.
class Table(ScrollableWidget):
    def __init__(self, parent, name, columns, 
                 row_height, rows_per_page, pixels_per_scroll=None):
        ScrollableWidget.__init__(self, parent, name)

        self.columns = []
        self.column = {}
        for column_name in columns:
            column = TableColumn(self, column_name)
            # keep an ordered list so we know how the columns go
            # left-to-right
            self.columns.append(column)
            # keep a hash so we can conveniently access columns by name
            self.column[column_name] = column

        self.row_height = row_height
        self.rows_per_page = rows_per_page
        if not pixels_per_scroll:
            # the sane default per scroll is exactly one row
            self.pixels_per_scroll = row_height

        self.clicks_per_row = 1
        if self.pixels_per_scroll != self.row_height:
            # FIXME
            # very naively calculate how many clicks we need to
            # do to scroll a row at a time
            if self.pixels_per_scroll < self.row_height:
                self.clicks_per_row *= self.row_height / self.pixels_per_scroll
            else:
                self.clicks_per_row /= self.pixels_per_scroll / self.row_height

    def capture_screenshots(self):
        for column in self.columns:
            column.capture_screenshots()
        # capture screenshots of the scrollbars, followed
        # finally by 'expected' cell states in the table itself
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

    def cell_exists(self, column_name, cell_value):
        if self.first_cell_where(**{column_name: cell_value}):
            return True
        return False

    # FIXME: make more efficient (short-circuit)
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
            rows.append(TableRow(self, cells, row_index))
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


# A column has cells, and cells make up rows. We'll always be searching
# by column to find rows, which entails looking up column cells and deducing
# which row the cells belong to
class TableColumn(Widget): 
    def __init__(self, table, name):
        Widget.__init__(self, table, name)
        self.table = table
        # create a button with the column name as its name
        # so that each column has its own subfolder within
        # the table's folder for state images
        self.header = Button(table, name)
        self.header_region = None

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
    # TODO: a cell value should be a folder of states/images rather
    #       than one image. FIX THIS!
    def next_cell_with(self, cell_value):
        self.table.scroll_to_top()
        self.locate_header()

        total_rows_scrolled = 0
        starting_cell = 0
        scanned_page = False
        while not self.table.scrollbar_at_bottom() or not scanned_page:
            for cur_cell in range(starting_cell, self.table.rows_per_page):
                y_offset = self.table.row_height + (cur_cell * self.table.row_height)
                cell_region = self.header_region.offset(Location(0, y_offset))
                cell_region.setH(self.table.row_height)
                cell_region = cell_region.nearby(self.table.row_height / 2)
                # hover over it as visual feedback
                cell_region.hover(cell_region)
                # look within region for cell value, performing
                # the search from the table so that cell value
                # is looked up within the table's image folder
                if self.table.do(cell_region, 'exists', cell_value):
                    if settings.DEBUG:
                        print "Found a cell matching '%s'" % cell_value
                    row_index = cur_cell + total_rows_scrolled
                    yield TableCell(self, 
                                    self.table.do(cell_region, 'find', cell_value), 
                                    row_index)
            scanned_page = True
            if not self.table.scrollbar_at_bottom():
                if settings.DEBUG:
                    print "Reached end of page, scrolling down one"
                rows_scrolled = self.table.scroll_down(self.table.rows_per_page)
                total_rows_scrolled += rows_scrolled
                starting_cell = self.table.rows_per_page - rows_scrolled
                scanned_page = False
        yield None

# FIXME: should cells be constructed, and THEN searched for?
class TableCell(Widget):
    """ A generated, "virtual" widget. Its region is actually a Match from
        a search performed in TableColumn.
    """
    def __init__(self, column, cell_match, row_index):
        Widget.__init__(self, column)
        self.region = cell_match
        self.column = column
        self.table = column.table
        self.row_index = row_index

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

    def __init__(self, table, cells, index):
        Widget.__init__(self, table)
        self.table = table
        self.cells = cells
        self.index = index

    def cell_under(self, column_name):
        cell = filter(lambda c: c.column.name == column_name, self.cells)
        if cell:
            return cell[0]
        return None

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
