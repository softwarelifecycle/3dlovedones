# replaced server address with var reference
import socket
import struct
import subprocess
import os
import logging

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


def snappicture(sock, address, local_ip, exp=11000):
    if os.path.exists(f'/home/pi/camera/{local_ip}_photo.jpg'):
        os.remove(f'/home/pi/camera/{local_ip}_photo.jpg')

    try:
        snapcmd = f'raspistill -ISO 100 -sa 30 -co 20 -q 75 -awb auto -ss {exp}  -o /home/pi/camera/{local_ip}_photo.jpg'

        sock.sendto(f"Camera CMD:{snapcmd}".encode('utf-8'), address)
        subprocess.call(snapcmd, shell=True)
        sock.sendto('TAKEN'.encode('utf-8'), address)

        sock.sendto("Running SCP!".encode('utf-8'), address)
        copyprocess = subprocess.Popen(["scp", f'/home/pi/camera/{local_ip}_photo.jpg',
                                        f'hchattaway@{address[0]}:/SSD500/Dropbox/Python/CommercialSites/3dlovedones/transfer/'])
        copyprocess.wait()
        # send ack!
        sock.sendto('FINISHED'.encode('utf-8'), address)
    except Exception as ex:
        logging.info(ex)
        sock.sendto(f"Error taking pic: {ex}".encode('utf-8'), address)


def main():
    logging.basicConfig(filename='camera.log', level=logging.INFO,  format='%(name)s - %(levelname)s - %(message)s')

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
                sock.sendto('Restarting Service!'.encode('utf-8'), address)
                cmd = 'sudo systemctl restart OnCamera.service'
                subprocess.call(cmd, shell=True)
            elif command == "ping":
                sock.sendto("PINGED".encode('utf-8'), address)
            elif command == "shutdown":
                sock.sendto("Shutting Down!".encode('utf-8'), address)
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
