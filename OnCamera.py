import socket
import struct
import subprocess
import sys

"""
Lives on the Raspberry Pi Zero.. is autostarted. 
This sends a message to the "RegisterCameras.py" listener which checks to make sure all cameras
are online!
"""

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007
destinationFolder = "test"
errorString = ""


def get_ip_address():
    host = socket.gethostname()
    ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
    return ipnum.strip()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
        data, address = sock.recvfrom(1024)
        data = data.decode('utf8')

        if data == "snap":
            cmd = f'raspistill -ISO 100 -sa 30 -co 20  -o /home/pi/camera/{local_ip}_photo.jpg'
            subprocess.call(cmd, shell=True)
            sock.sendto('TAKEN'.encode('utf8'), address)

            sock.sendto("Running SCP!".encode('utf8'), address)
            copyProcess = subprocess.Popen(["scp", f'/home/pi/camera/{local_ip}_photo.jpg',
                                            f'hchattaway@192.168.0.112:/SSD500/Dropbox/Python/CommercialSites/3dlovedones/transfer/'])
            sts = copyProcess.wait()
            # send ack!
            sock.sendto('FINISHED'.encode('utf8'), address)
        elif data == "reboot":
            sock.sendto('Restarting Service!'.encode('utf8'), address)
            cmd = 'sudo systemctl restart OnCamera.service'
            pid = subprocess.call(cmd, shell=True)
        elif data == "ping":
            sock.sendto("PINGED".encode('utf8'), address)

except:
    errorString = sys.exc_info()[0]
finally:
    sock.close()

# test change 2
