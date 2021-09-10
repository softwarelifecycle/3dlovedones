import socket
import struct
import subprocess
import fcntl
import os
import sys
from pathlib import Path

MCAST_GRP = '224.0.0.251'
MCAST_PORT = 5007
destinationFolder = "test"
errorString=""

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

local_ip = get_ip_address()


# Receive/respond loop
try:
    cmd = f'raspistill -o /home/pi/camera/{local_ip}_photo.jpg'
    subprocess.call(cmd, shell=True)
    copyProcess =  subprocess.Popen(["scp",f'/home/pi/camera/{local_ip}_photo.jpg',f'hchattaway@192.168.0.112:/SSD500/Dropbox/Python/CommercialSites/3dlovedones/clients/{destinationFolder}/'])
    sts = copyProcess.wait()
except:
    errorString = sys.exc_info()[0]
    print("errorString")
finally:
    print("Closing Socket")
    sock.close()
