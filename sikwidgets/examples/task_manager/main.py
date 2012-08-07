from sikwidgets import settings
from task_manager import TaskManager

def main():
    # The default directory Sikwidgets looks into
    # for images of widgets can be changed.
    # This is useful if the same application has
    # different looks across OSs.
    #
    settings.IMAGES_PATH = "images-winxp-default"

    # More status messages 
    # will be printed to the screen and windows, widgets,
    # and mouse actions will be highlighted.
    # Note: The program will run significantly slower.
    #
    settings.debug()

    # This setting changes how much an image is compacted
    # for processing as well as slightly changing the 
    # similarity threshold for finding image matches.
    #
    # settings.accuracy_low()
    # settings.accuracy_med()
    settings.accuracy_high()

    # Pretty self-explanatory.
    # 
    # settings.mouse_speed_slow()
    # settings.mouse_speed_med()
    settings.mouse_speed_fast()

    tm = TaskManager()
    # Explicitly open the app by running the open_cmd
    tm.open()

    # Wait 5 seconds before scanning the focused
    # window to see if it matches the description
    # of any of the defined Windows in the app.
    # If it does, the appropriate window is instantiated
    # and returned. Otherwise, this will be None.
    tasks = tm.focused_window(5)
    if not tasks:
        print "Task Manager window not found"
        return

    # Have some fun with the window :)
    tasks.applications_tab.click()
    tasks.processes_tab.click()
    tasks.processes_table.column['user_name'].click()
    tasks.processes_table.column['cpu'].click()
    tasks.processes_table.column['memory'].click()
    tasks.processes_table.column['image_name'].click()
    # Since there is no java.exe.png file under the
    # processes_table folder, looking for 'java.exe'
    # will result in the text of each row being read
    # (using Sikuli's OCR) and compared against what
    # we specified.
    cell = tasks.processes_table.column['image_name'].first_cell_with('java.exe')
    # If we found a 'java.exe' cell, click it!
    if cell:
        cell.click()


if __name__ == "__main__":
    main()