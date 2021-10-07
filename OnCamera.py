# replaced server address with var reference
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

def snappicture(address, local_ip):
    snapcmd = f'raspistill -ISO 100 -sa 30 -co 20  -o /home/pi/camera/{local_ip}_photo.jpg'
    sock.sendto(f"Camera CMD:{snapcmd}".encode('utf-8'), address)

    subprocess.call(snapcmd, shell=True)
    sock.sendto('TAKEN'.encode('utf-8'), address)

    sock.sendto("Running SCP!".encode('utf-8'), address)
    copyprocess = subprocess.Popen(["scp", f'/home/pi/camera/{local_ip}_photo.jpg',
                                    f'hchattaway@{address[0]}:/SSD500/Dropbox/Python/CommercialSites/3dlovedones/transfer/'])
    sts = copyprocess.wait()
    # send ack!
    sock.sendto('FINISHED'.encode('utf-8'), address)

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
        data = data.decode('utf-8')
        sock.sendto(f'Data on Camera: {data}'.encode('utf-8'), address)

        # take pic if broadcast to all or just this one!
        if data == "snap" or data == local_ip:
            snappicture(address, local_ip)

        elif data == "restart":
            sock.sendto('Restarting Service!'.encode('utf-8'), address)
            cmd = 'sudo systemctl restart OnCamera.service'
            pid = subprocess.call(cmd, shell=True)
        elif data == "ping":
            sock.sendto("PINGED".encode('utf-8'), address)
        elif data == "shutdown":
            sock.sendto("Shutting Down!".encode('utf-8', address))
            cmd = 'sudo shutdown -h now'
            pid = subprocess.call(cmd, shell=True)
        elif data == 'reboot':
            cmd = 'sudo shutdown -r 0'
            pid = subprocess.call(cmd, shell=True)

except:
    errorString = sys.exc_info()[0]
finally:
    sock.close()


