import socket
import struct
import subprocess
import fcntl
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
   return ipnum
 

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

# Receive/respond loop
try:
    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        data = data.decode('utf8')
        if data == "snap":
            print("Taking Picture!")
            cmd = 'raspistill -o /home/pi/camera/photo.jpg ' 
            print(get_ip_address())
        elif data == "reboot":
            print("rebooting...")
            cmd = 'sudo reboot'
            pid = subprocess.call(cmd, shell=True)

finally:
    print("Closing Socket")
    sock.close()
