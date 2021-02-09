import socket
import struct

"""
Sits on laptop waiting to hear from camera's as they are powered up. Just used to make sure all cameras are online before triggering them.
"""

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007

registered_cameras = 0
max_cameras = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print("\n Waiting for Camera's to Register!")

# Receive/respond loop
while True:
    data, address = sock.recvfrom(1024)
    data = data.decode('utf8')
    if data == 'REGISTER':
        registered_cameras += 1
        print(f"Total Cameras Registered: {registered_cameras} out of {max_cameras} at {address}")

    if registered_cameras == max_cameras:
        break

sock.close()
