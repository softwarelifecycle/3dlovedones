import PySimpleGUI as sg
import socket
import subprocess
import utilities
import os
import glob
import TriggerCameras

cameras = [[1, "192.168.0.106", "192.168.0.106_image.jpg"]]
cameras.append([2, "192.168.0.107", "192.168.0.107_image.jpg"])
cameras.append([3, "192.168.0.108", "192.168.0.108_image.jpg"])
cameras.append([4, "192.168.0.109", "192.168.0.109_image.jpg"])
print(f"Cameras = {cameras}")

DESTINATION_PATH = ""
HOME = "/SSD500/Dropbox/Python/CommercialSites/3dlovedones/"
MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007

def make_window(theme):
    """"
    Create layout for main window!
    """
    sg.theme(sg.OFFICIAL_PYSIMPLEGUI_THEME)

    headings = [["Camera #"], ["IP Address"], ["Image"]]

    # layout in columns
    main_tab_left_column = [
        [sg.Frame(layout=[
            [sg.Text("# of Cameras")],
            [sg.Spin([i for i in range(1, 100)], initial_value=10, k='-CAMERACOUNT-', size=(10, 10))],
            [sg.Text("Server IP Address")],
            [sg.Input(key="-IPADDRESS-", size=(15, 2))],
            [sg.Text("Destination", font='Rasa 12')],
            [sg.Input(key='-DESTTEXT-', size='20', default_text='Select Folder...', expand_x=True),
             sg.FolderBrowse(key="-DESTINATION-", target='-DESTTEXT-')]],
            title="Settings", expand_x=True, pad=(10, 5))],
        [sg.Frame(layout=[
            [sg.Button('Update Camera Code', key="-UPDATECODE-", font='Rasa 12', size=20)],
            [sg.Button('ReBoot Cameras', key="-REBOOT-", font='Rasa 12', size=20)], \
            [sg.Button('Ping Cameras', key="-PING-", font='Rasa 12', size=20)],
            [sg.Button('Delete Transfer Folder Pics', key="-DELETETRANSFERFOLDER-", font='Rasa 12', size=20)],
            [sg.Button('Take Pictures!', key="-SNAP-", font='Rasa 12', size=20)],
            [sg.Button('Delete Pics On Cameras', key="-DELETECAMERAPICS-", font='Rasa 12', size=20)],
            [sg.Button('Exit', font='Rasa 12', size=20)]], title="Actions", expand_x=True, pad=(10, 5))]]

    main_tab_right_column = [[sg.Table(values=cameras, headings=headings, max_col_width=25,
                                       # background_color='light blue',
                                       justification='right',
                                       num_rows=4,
                                       auto_size_columns=True,
                                       expand_x=True,
                                       alternating_row_color='gray',
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

    layout = [[sg.Text('3D Loved Ones Model Generator', font='Rasa 40', justification='center', expand_x=True,
                       relief="raised")]]
    # layout = [[sg.Image(filename="3dTitle.png", key='image')]]
    layout += [[sg.TabGroup([[sg.Tab('Main', tab_layout), sg.Tab('Theme', theme_layout)]], key='-TAB GROUP-',
                            size=(1990, 790))]]
    return sg.Window('3D Loved Ones', layout, size=(1600, 800), location=(100, 100), resizable=True, finalize=True)


def updatecode():
    """
    Copy the OnCamera.py file to the registered cameras
    """
    camera_ip = "192.168.0.106"

    copyCameraCode = subprocess.Popen(
        ["scp", '/SSD500/Dropbox/Python/CommercialSites/3dlovedones/OnCamera.py', f'pi@{camera_ip}:/home/pi/listener/'])
    returncode = copyCameraCode.wait()
    print(f"return code: {returncode}")

    if returncode != 0:
        sg.popup_error("Transfer did not complete!")
    else:
        sg.popup("Transfer completed!")


def rebootcameras():
    """
    reboot all registered cameras.. Usually done after calling the "UpdateCode" method 
    """
    rebootCamera = subprocess.Popen(
        ["ssh", 'sudo reboot', f'pi@{camera_ip}'])
    returncode = rebootcamera.wait()
    print(f"return code: {returncode}")

    print("Clicked Reboot")

def pingcameras():
    TriggerCameras.ping(MCAST_GRP, MCAST_PORT)

def snap(destination_path):
    """
    Send the SNAP command to the camera's to take a pic and then upload.
    """
    print(f"Destination Path={destination_path}")
    if len(destination_path.strip()) == 0:
        sg.popup('Supply File Destination!')
    else:
        TriggerCameras.snap(MCAST_GRP,  MCAST_PORT)

def deletetransferpics(home):
    print(f"Home: {home}")
    for f in glob.glob("transfer/*.jpg"):
        print(f"File: {f}")
        os.remove(f)


def deletecamerapics():
    """
    Delete the pics on all registered cameras.
    """
    print("Clicked Delete Camera pics")


def main():
    """
    Entry point for creating view
    """
    window = make_window(sg.theme("Light Blue 2"))
    SERVER_IP = utilities.get_ip_address()
    window['-IPADDRESS-'].update(SERVER_IP)

    # This is an Event Loop 
    while True:
        event, values = window.read()
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
            rebootcameras()
        elif event == "-SNAP-":
            DESTINATION_PATH = values['-DESTINATION-']
            snap(DESTINATION_PATH)
        elif event == "-DELETECAMERAPICS-":
            deletecamerapics()
        elif event == '-DELETETRANSFERFOLDER-':
            deletetransferpics(HOME)
        elif event == "-PING-":
            pingcameras()

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
