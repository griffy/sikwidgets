from sikwidgets import settings
from task_manager import TaskManager

def main():
    # settings.IMAGES_PATH = "images"
    # settings.debug()
    settings.accuracy_high()
    settings.mouse_speed_fast()

    tm = TaskManager()
    tm.open()

    tasks = tm.focused_window(10)

    tasks.applications_tab.click()
    tasks.processes_tab.click()
    tasks.processes_table.column['user_name'].click()
    tasks.processes_table.column['cpu'].click()
    tasks.processes_table.column['memory'].click()
    tasks.processes_table.column['image_name'].click()
    cell = tasks.processes_table.column['image_name'].first_cell_with('java.exe')
    if cell:
        cell.click()


if __name__ == "__main__":
    main()