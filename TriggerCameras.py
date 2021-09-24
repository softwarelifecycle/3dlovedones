# Multicast sender
# Guidance:  https://stackoverflow.com/a/1794373
import UtilityFunctions

def rebootcameras(mcast_grp, mcast_port):
    sock = UtilityFunctions. getsocket()
    message = b'reboot'
    sock.sendto(message, (mcast_grp, mcast_port))
    sock.close()


def ping(mcast_grp, mcast_port):
    """
    Just ping cameras via multicast and get response.
    """
    sock = UtilityFunctions. getsocket()
    message = b'ping'
    server = ""
    numcameras = 0
    try:
        print('sending {!r}'.format(message))
        sock.sendto(message, (mcast_grp, mcast_port))
        print('waiting for ping ack...')
        while True:
            try:
                data, server = sock.recvfrom(200)
                data = data.decode('utf8')
                print(f'Ping Data Returned: {data}')
                if data == 'PINGED':
                    print(f'PINGED! by {server[0]}')
                    numcameras += 1
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


def snap(mcast_grp, mcast_port, window):
    """
    Send the "snap" keyword via multicast and wait for responses.... This will add each response to the cameras list.
    """
    sock = UtilityFunctions. getsocket()
    message = b'snap'
    server = ""
    numcameras = 0
    try:
        # Send data to the multicast group
        sock.sendto(message, (mcast_grp, mcast_port))
        print('sent snap command,   waiting for snap  ack...')
        while True:
            try:
                data, server = sock.recvfrom(200)
                data = data.decode('utf8')
                print(f'Snap Data: {data}')
                if data == 'TAKEN':
                    print(f'Pic Taken by {server[0]}')

                if data != 'TAKEN' and data != "FINISHED":
                    print(f'{data}')

                if data == 'FINISHED':
                    numcameras += 1
                    window.write_event_value('-PICTURETAKEN-', (numcameras, server[0], f"{server[0]}_photo.jpg"))
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
