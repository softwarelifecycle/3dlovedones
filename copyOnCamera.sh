#!/bin/bash

 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.100:/home/pi/listener
 #scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.101:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.102:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.103:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.104:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.105:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.106:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.107:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.108:/home/pi/listener
 scp -o StrictHostKeyChecking=no OnCamera.py pi@192.168.0.109:/home/pi/listener

echo "re-starting services on  cameras..."
 ssh pi@192.168.0.100 'sudo systemctl restart OnCamera.service'
 #ssh pi@192.168.0.101 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.102 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.103 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.104 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.105 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.106 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.107 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.108 'sudo systemctl restart OnCamera.service'
 ssh pi@192.168.0.109 'sudo systemctl restart OnCamera.service'

