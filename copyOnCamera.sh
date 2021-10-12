#!/bin/bash

scp OnCamera.py pi@192.168.0.100:/home/pi/listener
scp OnCamera.py pi@192.168.0.117:/home/pi/listener
scp OnCamera.py pi@192.168.0.106:/home/pi/listener
scp OnCamera.py pi@192.168.0.114:/home/pi/listener
scp OnCamera.py pi@192.168.0.115:/home/pi/listener
scp OnCamera.py pi@192.168.0.113:/home/pi/listener
scp OnCamera.py pi@192.168.0.110:/home/pi/listener
scp OnCamera.py pi@192.168.0.101:/home/pi/listener
scp OnCamera.py pi@192.168.0.116:/home/pi/listener
scp OnCamera.py pi@192.168.0.108:/home/pi/listener

echo "rebooting cameras..."
 ssh pi@192.168.0.100 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.117  'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.106 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.114 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.115 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.113 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.110 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.101 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.116 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.108 'sudo systemctl restart OnCamera.service'

