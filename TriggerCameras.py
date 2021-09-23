# Multicast sender
# Guidance:  https://stackoverflow.com/a/1794373
import socket
import UtilityFunctions


def getsocket():
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    return sock


def rebootcameras(mcast_grp, mcast_port):
    sock = getsocket()
    message = b'reboot'
    sock.sendto(message, (mcast_grp, mcast_port))
    sock.close()


def ping(mcast_grp, mcast_port):
    """
    Just ping cameras via multicast and get response.
    """
    sock = getsocket()
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

            except socket.timeout:
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
    sock = getsocket()
    message = b'snap'
    server = ""
    numcameras = 0
    try:
        # Send data to the multicast group
        print('sending {!r}'.format(message))
        sock.sendto(message, (mcast_grp, mcast_port))
        print('waiting for snap  ack...')
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

            except socket.timeout:
                print('timed out, no more responses')
                break

    except:
        print("Problem sending trigger!")

    finally:
        print('closing socket')
        sock.close()
    return numcameras
