import os
import subprocess
p = subprocess.Popen(["scp", "/SSD500/Dropbox/Python/CommercialSites/3dlovedones/OnCamera.py","pi@192.168.0.106:./"])
sts = os.waitpid(p.pid, 0)
