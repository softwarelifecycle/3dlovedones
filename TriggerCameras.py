# Multicast sender
# Guidance:  https://stackoverflow.com/a/1794373
import UtilityFunctions
import time


def restartcameras(mcast_grp, mcast_port):
    sock = UtilityFunctions.getsocket()
    message = b'restart'
    sock.sendto(message, (mcast_grp, mcast_port))
    sock.close()


def rebootcameras(mcast_grp, mcast_port):
    sock = UtilityFunctions.getsocket()
    message = b'reboot'
    sock.sendto(message, (mcast_grp, mcast_port))
    sock.close()

def shutdowncameras(mcast_grp, mcast_port):
    sock = UtilityFunctions.getsocket()
    message = b'shutdown'
    sock.sendto(message, (mcast_grp, mcast_port))
    sock.close()


def ping(mcast_grp, mcast_port, max_cameras, window):
    """
    Just ping cameras via multicast and get response.
    """
    sock = UtilityFunctions.getsocket()
    message = b'ping'
    server = ""
    numcameras = 0
    try:
        print('sending {!r}'.format(message))
        start = time.time()
        sock.sendto(message, (mcast_grp, mcast_port))
        print('waiting for ping ack...')
        while True:
            try:
                print("Waiting on recvfrom...")
                data, camaddress = sock.recvfrom(200)
                data = data.decode('utf-8')
                print(f'Ping Data Returned: {data}')
                print(time.time() - start)

                if data == 'PINGED':
                    print(f'PINGED! by {camaddress[0]}')
                    numcameras += 1
                    window.write_event_value('-CAMERAPINGED-', (numcameras, camaddress[0], ""))

                if numcameras == max_cameras:
                    break

            except sock.timeout:
                print('timed out, no more responses')
                break
    except:
        print("Problem sending trigger!")

    finally:
        print('closing socket')
        sock.close()

    return numcameras


def snap(mcast_grp, mcast_port, window, max_cameras, cameraip = ''):
    """
    Send the "snap" keyword via multicast and wait for responses.... This will add each response to the cameras list.
    """
    sock = UtilityFunctions.getsocket()
    if len(cameraip) != 0:
        message = cameraip.encode('utf-8')
    else:
        message = b'snap'

    server = ""
    numcameras = 0
    try:
        # Send data to the multicast group
        sock.sendto(message, (mcast_grp, mcast_port))
        print(f'sent snap command {message},   waiting for snap  ack...')
        while True:
            try:
                data, server = sock.recvfrom(200)
                data = data.decode('utf-8')
                print(f'Snap Data: {data}')
                if data == 'TAKEN':
                    print(f'Pic Taken by {server[0]}')

                if data != 'TAKEN' and data != "FINISHED":
                    print(f'{data}')

                if data == 'FINISHED':
                    numcameras += 1
                    window.write_event_value('-PICTURETAKEN-', (numcameras, server[0], f"{server[0]}_photo.jpg"))

                    if numcameras == max_cameras:
                        break

            except sock.timeout:
                print('timed out, no more responses')
                break

    except:
        print("Problem sending trigger!")

    finally:
        print('closing socket')
        sock.close()
    return numcameras
