import socket
import struct
import subprocess
import fcntl
import os
from ftplib import FTP
from pathlib import Path

"""
Lives on the Raspberry Pi Zero.. is autostarted. 
This sends a message to the "RegisterCameras.py" listener which checks to make sure all cameras
are online!
"""

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007
IS_ALL_GROUPS = False


def get_ip_address():
    host = socket.gethostname()
    ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
    return ipnum.strip()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# register this camera with server!  Want to make sure all camera's are online before taking pic.
MESSAGE = bytes("REGISTER", "utf-8")
sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))
local_ip = get_ip_address()

# Receive/respond loop
try:
    while True:
        print('\nwaiting for command...')
        data, address = sock.recvfrom(1024)
        data = data.decode('utf8')

        if data == "snap":
            cmd = f'raspistill -o /home/pi/camera/{local_ip}_photo.jpg'
            subprocess.call(cmd, shell=True)
            sock.sendto(b'TAKEN', address)
            file_path = Path(f'/home/pi/camera/{local_ip}_photo.jpg')
            with FTP('192.168.1.233', '3duser', '3duser') as ftp, open(file_path, 'rb') as file: ftp.storbinary(f'STOR {file_path.name}', file)
            sock.sendto(b'FINISHED', address)

        elif data == "reboot":
            cmd = 'sudo reboot'
            pid = subprocess.call(cmd, shell=True)

finally:
    print("Closing Socket")
    sock.close()
