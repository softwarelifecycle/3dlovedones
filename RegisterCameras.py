import socket
"""
Sits on laptop waiting to hear from camera's as they are powered up. Just used to make sure all cameras are online before triggering them.
"""

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007
MULTICAST_TTL = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sock.bind((MCAST_GRP, MCAST_PORT))

def registercameras(max_cameras, window):
    """
    Listen for cameras to broadcast that they booted up...
    """
    registered_cameras = 0
    # Receive/respond loop
    while True:
        data, camaddress = sock.recvfrom(1024)
        data = data.decode('utf8')
        if data == 'REGISTER':
            registered_cameras += 1
            window['-STATUSTEXT-'].update( f"Registered {registered_cameras} Cameras!")
            print(f"Registered {registered_cameras} cameras!")
            window.write_event_value('-CAMERAREGISTERED-', (registered_cameras, camaddress[0], ""))

        if registered_cameras == max_cameras:
            break

    sock.close()

    return registercameras
