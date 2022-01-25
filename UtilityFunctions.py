import os.path
from pathlib import Path
import shutil
import socket
import subprocess
import re
from os.path import exists

def get_ip_address():
    #host = socket.gethostname()
    ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
    return ipnum.split()[0].strip()


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

def copyfiles(src_path, trg_path, just_single_pic = False):
    """
    while copying files if a file exists, increment till it doesnt' appear.
    """
    filecnt = 0
   
    new_name = src_path
    dest_file = trg_path

    print(f"In Copyfiles Dest: {dest_file}!")
    if just_single_pic == False:
        found = exists(dest_file)
        while found:
            new_name = re.sub('(_photo)([0-9]{2})', increment, f'{dest_file}')
            dest_file = new_name
            found = exists(dest_file)
            
    print(f'Source: {src_path} Dest: {dest_file}')
    shutil.copy(f'{src_path}', dest_file)
    
    filecnt += 1
        
    return new_name


def increment(num):
    # Return the first match which is 'E'. Return the 2nd match + 1 which is 'x + 1'
    return num.group(1) + str(int(num.group(2)) + 1).zfill(2)


def getsocket():
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    return sock
