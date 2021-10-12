import subprocess
snapcmd = f'raspistill -ISO 100 -sa 30 -co 20  -o /home/pi/camera/192.168.0.116_photo.jpg'
subprocess.call(snapcmd, shell=True)

