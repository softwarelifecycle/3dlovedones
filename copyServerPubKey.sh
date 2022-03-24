#!/bin/bash

scp -o StrictHostKeyChecking=no /home/hchattaway/.ssh/pubkeyforcamera/id_rsa.pub  pi@192.168.0.104:/home/pi

