# replaced server address with var reference
import socket
import struct
import subprocess
import os
import logging
import re
import glob

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
    ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
    return ipnum.strip()


def increment(num):
    # Return the first match which is 'E'. Return the 2nd match + 1 which is 'x + 1'
    return num.group(1) + str(int(num.group(2)) + 1).zfill(2)


def snappicture(socket, address, local_ip, exp=11000):
    # Getting the list of directories
    path = "/home/pi/camera"
    picturedir = os.listdir(path)

    # Check to see of folder empty.. if it is, start off at "01"... if not use that to start the numbering.
    if len(picturedir) == 0:
        filename = f'{path}/{local_ip}_photo01.jpg'
    else:
        filename = re.sub('(_photo)([0-9]{2})', increment, f'{path}/{picturedir[0]}')

    try:
        snapcmd = f'raspistill -ISO 100 -sa 30 -co 20 -q 100 -awb auto -ss {exp}  -o {filename}'

        logging.info(f'snapcmd: {snapcmd}')

        socket.sendto(f"Camera CMD:{snapcmd}".encode('utf-8'), address)
        subprocess.call(snapcmd, shell=True)
        socket.sendto('TAKEN'.encode('utf-8'), address)

        socket.sendto("Running SCP!".encode('utf-8'), address)
        copycmd = f'scp -o StrictHostKeyChecking=no {filename}  hchattaway@{address[0]}:/home/hchattaway/Dropbox/Python/CommercialSites/3dlovedones/transfer'
        subprocess.call(copycmd, shell=True)

        # send ack!
        socket.sendto('FINISHED'.encode('utf-8'), address)
    except Exception as ex:
        logging.info(ex)
        socket.sendto(f"Error taking pic: {ex}".encode('utf-8'), address)


def deletepics():
    for f in glob.glob("/home/pi/camera/*.jpg"):
        os.remove(f)


def main():
    deletepics()
    logging.basicConfig(filename='camera.log', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # register this camera with server!  Want to make sure all camera's are online before taking pic.
    MESSAGE = "REGISTER".encode("UTF-8")
    sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))
    local_ip = get_ip_address()
    logging.info(f'Registering Camera!')

    # Receive/respond loop
    try:
        while True:
            data, address = sock.recvfrom(1024)
            logging.info(f'data: {data}  Address: {address}')
            splitdata = data.decode("UTF-8").split(":")
            logging.info(f'SplitData: {splitdata}')
            command = splitdata[0]
            if command == 'REGISTER':
                continue

            exposure = int(splitdata[1])

            logging.info(f'Command: {command}  Exposure: {exposure}')
            sock.sendto(f'Data on Camera: {command} Exposure: {exposure}'.encode('UTF-8'), address)

            # take pic if broadcast to all or just this one!
            if command == "snap" or command == local_ip:
                snappicture(sock, address, local_ip, exposure)

            elif command == "restart":
                sock.sendto('Restarting Service!'.encode('UTF-8'), address)
                cmd = 'sudo systemctl restart OnCamera.service'
                subprocess.call(cmd, shell=True)
            elif command == "ping":
                logging.info(f'Sending PINGED ack to {address}!')
                sock.sendto("PINGED".encode('UTF-8'), address)
            elif command == "shutdown":
                sock.sendto("Shutting Down!".encode('UTF-8'), address)
                cmd = 'sudo shutdown -h now'
                subprocess.call(cmd, shell=True)
            elif command == 'reboot':
                cmd = 'sudo shutdown -r 0'
                subprocess.call(cmd, shell=True)

    except Exception as ex:
        logging.info(ex, exc_info=True)
    finally:
        sock.close()


if __name__ == '__main__':
    main()
