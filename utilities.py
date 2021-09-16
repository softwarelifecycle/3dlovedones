import socket
import subprocess

def get_ip_address():
    host = socket.gethostname()
    ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
    return ipnum.split()[0].strip()