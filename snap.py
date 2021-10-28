import subprocess
snapcmd = 'raspistill -ISO 100 -sa 30 -co 20 -q 75 -awb auto -ss 8000  -o /home/pi/camera/snaptest.jpg'
subprocess.call(snapcmd, shell=True)

copycmd = 'scp  -o StrictHostKeyChecking=no  /home/pi/camera/snaptest.jpg hchattaway@192.168.0.123:/home/hchattaway/Dropbox/Python/CommercialSites/3dlovedones/transfer'
subprocess.call(copycmd, shell=True)





