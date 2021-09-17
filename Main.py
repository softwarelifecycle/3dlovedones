import PySimpleGUI as sg
import socket
import subprocess
import utilities

DATA = [[j for j in range(5)] for i in range(10)]


def make_window(theme):
    """"
    Create layout for main window!
    """
    sg.theme(theme)

    headings = [["Camera #"], ["IP Address"], ["Picture Taken"], ["Uploaded"], ["Image"]]
    # layout in columns
    main_tab_left_column = [
        [sg.Frame(layout=[
            [sg.Text("# of Cameras")],
            [sg.Spin([i for i in range(1, 100)], initial_value=10, k='-CAMERACOUNT-', size=(10, 10))],
            [sg.Text("Server IP Address")],
            [sg.Input(key="-IPADDRESS-", size=(15, 2))]], title="Settings", expand_x=True, pad=(10, 5))],
        [sg.Frame(layout=[
            [sg.Button('Update Camera Code', key="-UPDATECODE-", size=(20, 2))],
            [sg.Button('ReBoot Cameras', key="-REBOOT-", size=(20, 2))],
            [sg.Button('Take Pictures!', key="-SNAP-", size=(20, 2))],
            [sg.Button('Delete Pics On Cameras', key="-DELETECAMERAPICS-", size=(20, 2))],
            [sg.Button("Picture Destination", key="-DESTINATION-", size=(20, 2))],
            [sg.Button('Exit', size=(20, 2))]], title="Actions", expand_x=True, pad=(10, 5))]]

    main_tab_right_column = [[sg.Table(values=DATA, headings=headings, max_col_width=25,
                                       # background_color='light blue',
                                       justification='right',
                                       num_rows=20,
                                       def_col_width=30,
                                       expand_x=True,
                                       alternating_row_color='lightyellow',
                                       key='-CAMERATABLE-',
                                       row_height=35,
                                       tooltip='Camera Listing')]]

    tab_layout = [[sg.Col(main_tab_left_column, vertical_alignment='top', pad=(0, 0)),
                   sg.Col(main_tab_right_column, vertical_alignment='top', expand_x=True)]]

    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values=sg.theme_list(),
                                size=(20, 12),
                                key='-THEME LISTBOX-',
                                enable_events=True)],
                    [sg.Button("Set Theme")]]

    # ,[sg.Text("3D Model Generator",font=("newspaper", 32))]
    layout = [[sg.Image(filename="3dTitle.png", key='image')]]
    layout += [[sg.TabGroup([[sg.Tab('Main', tab_layout), sg.Tab('Theme', theme_layout)]], key='-TAB GROUP-',
                            size=(1990, 790))]]
    return sg.Window('3D Loved Ones', layout, size=(1800, 800), location=(100, 100), resizable=True, finalize=True)


def updatecode():
    """
    Copy the OnCamera.py file to the registered cameras
    """
    print("Clicked Update Code")


def rebootcamera():
    """
    reboot all registered cameras.. Usually done after calling the "UpdateCode" method 
    """
    print("Clicked Reboot")


def snap(DESTINATION_PATH=None):
    """
    Send the SNAP command to the camera's to take a pic and then upload.
    """
    if len(DESTINATION_PATH.strip()) == 0:
        DESTINATION_PATH = sg.popup_get_folder("Select Destination folder first!")

    print("Clicked Snap!")


def deletecamerapics():
    """
    Delete the pics on all registered cameras.
    """
    print("Clicked Delete Camera pics")


def destination():
    """
    Change the destination folder for the pics coming from the cameras
    """
    DESTINATION_PATH = sg.popup_get_folder("Select Destination folder...")


def main():
    """
    Entry point for creating view
    """
    window = make_window(sg.theme("Light Blue 2"))
    SERVER_IP = utilities.get_ip_address()
    window['-IPADDRESS-'].update(SERVER_IP)
    DESTINATION_PATH = ""

    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        # window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            okToLeave = sg.popup_yes_no("Do you really want to leave?", title="Exit?", keep_on_top=True)
            if okToLeave == "Yes":
                break
        elif event == 'About':
            sg.popup('PySimpleGUI Demo All Elements',
                     'Right click anywhere to see right click menu',
                     'Visit each of the tabs to see available elements',
                     'Output of event and values can be see in Output tab',
                     'The event and values dictionary is printed after every event')
        elif event == "Open Folder":
            folder_or_file = sg.popup_get_folder('Choose your folder')
        elif event == "Set Theme":
            theme_chosen = values['-THEME LISTBOX-'][0]
            window.close()
            window = make_window(theme_chosen)
        elif event == "-UPDATECODE-":
            updatecode()
        elif event == "-REBOOT-":
            rebootcamera()
        elif event == "-SNAP-":
            snap(DESTINATION_PATH)
        elif event == "-DELETECAMERAPICS-":
            deletecamerapics()
        elif event == "-DESTINATION-":
            destination()

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
