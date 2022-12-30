import os
import PySimpleGUI as sg
import logging
# Root directory of file
mypath = ''

# Special characters that will be changed
old_skin_number = 'C06'

# Special characters to change
new_skin_number = 'C07'

# Depending on operating system
WINDOWS_PATH = '\\'
MAC_PATH = '/'


# Enable logging
logging.basicConfig(filename="log.txt", level=logging.INFO)


def hasOldSkin(element):
    if old_skin_number in element:
        return True
    return False


def getOldSkinFiles():
    old_files = []
    for path, currentDirectory, files in os.walk(mypath):

        for d in currentDirectory:
            if hasOldSkin(d):
                old_files.append(d)
        for file in files:
            if hasOldSkin(file):
                old_files.append(file)
    return old_files


def getCurrentDirectory(path):
    split_path = path.split('/')
    return split_path[len(split_path) - 1]


def main():
    CHANGED = ''
    old_files = getOldSkinFiles()
    while(len(old_files) > 0):
        curr_file = old_files.pop()
        for path, currentDirectory, files in os.walk(mypath):
            if curr_file in files:
                old_path = path + MAC_PATH + curr_file
                new_path = path + MAC_PATH + \
                    curr_file.replace(old_skin_number, new_skin_number)
                log = str(old_path) + ' -> ' + str(new_path)
                CHANGED = CHANGED + (log + '\n')
                logging.info(str(old_path) + ' -> ' + str(new_path))
                os.rename(old_path, new_path)
                break
            curr_dir = getCurrentDirectory(path)
            if curr_file in curr_dir:
                new_skin_element = curr_dir.replace(
                    old_skin_number, new_skin_number)
                new_path = path.replace(curr_dir, new_skin_element)
                log = str(path) + ' -> ' + str(new_path)
                CHANGED = CHANGED + (log + '\n')
                logging.info(log)
                os.rename(path, new_path)
                break
    return CHANGED


# main()


layout = [[sg.Text("Old Skin Number")],
          [sg.Input()],
          [sg.Text("New Skin Number")],
          [sg.Input()],
          [sg.Text("Absolute Path to Directory")],
          [sg.Input()],
          [sg.Button('Ok')],
          [sg.Button('Quit')]]

window = sg.Window('Smash Mod File Automation Tool', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == 'Ok':
        old_skin_number = values[0]
        new_skin_number = values[1]
        mypath = values[2]
        try:
            logs = main()
            text_file = open("log.txt", "r")
            data = text_file.read()
            sg.popup("Success: \n " + logs)
            text_file.close()
        except Exception as e:
            sg.popup_error_with_traceback(
                f'An error happened.  Here is the info:', e)
