import PySimpleGUI as sg

def make_window(theme):
    sg.theme(theme)

    main_layout = [
                  [sg.Frame(layout=[
                  [sg.Text("# of Cameras")],
                  [sg.Spin([i for i in range(1,100)], initial_value=10, k='-CAMERACOUNT-',size=(10,10))], 
                  [sg.Text("Server IP Address")],
                  [sg.Input(key="IPAddress",size=(16,2))]],title="Settings")],
                  [sg.Frame(layout=[
                  [sg.Button('Update Camera Code', size=(20,2))],
                  [sg.Button('ReBoot Cameras',size=(20,2))],
                  [sg.Button('Take Pictures!',size=(20,2))],
                  [sg.Button('Delete Pics On Cameras',size=(20,2))],
                  [sg.Button("Picture Destination",size=(20,2))],
                  [sg.Button('Exit',size=(20,2))]],title="Actions")]]

    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values = sg.theme_list(), 
                      size =(20, 12), 
                      key ='-THEME LISTBOX-',
                      enable_events = True)],
                      [sg.Button("Set Theme")]]
    
    layout = [[sg.Image(filename="3dTitle.png", key='image')]]
    layout +=[[sg.TabGroup([[  sg.Tab('Main', main_layout), 
                               sg.Tab('Theme', theme_layout)
                               ]], key='-TAB GROUP-', size=(1990, 790))]]
              
    return sg.Window('3D Loved Ones', layout, size=(1800, 800),location=(100,100), resizable=True)


def main():
    window = make_window(sg.theme("Light Blue 2"))
    
    # This is an Event Loop 
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        # window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
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

    window.close()
    exit(0)

if __name__ == '__main__':
    main()