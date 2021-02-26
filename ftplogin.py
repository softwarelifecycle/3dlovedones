import ftplib
ftp = ftplib.FTP()
host = "192.168.1.233"
port = 21
ftp.connect(host, port)
print (ftp.getwelcome())
try:
    print ("Logging in...")
    ftp.login("3duser","3duser")
except:
    print("failed to login")

