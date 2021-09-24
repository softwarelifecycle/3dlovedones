from pathlib import Path
import shutil
import socket

def tryparse(string, base=10):
    """
        Usage:>>> if (n := tryparse("123")) is not None:
    ...     print(n)
    ...
    123
     if (n := tryparse("abc")) is None:
    ...     print(n)
    None
    """

    try:
        return int(string, base=base)
    except ValueError:
        return None

def copyfiles(src_path, trg_path):
    filecnt = 0
    for src_file in Path(src_path).glob('*.*'):
        print(f'Src Path: {src_path},   File= {src_file},  Dest Path={trg_path}')
        shutil.copy(src_file, trg_path)
        filecnt += 1
    return filecnt

def getsocket():
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    return sock