#!/usr/bin/env python
import subprocess
import socket

# configure the serial connection
host = socket.gethostname()
ipnum = subprocess.check_output(["hostname", "-I"]).decode("utf-8")

print(f"IP Number: {ipnum}")

