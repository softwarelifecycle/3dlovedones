from ftplib import FTP
from pathlib import Path

file_path = Path('/home/hchattaway/Pictures/MineFalls.jpg')

with FTP('192.168.1.233', '3duser', '3duser') as ftp, open(file_path, 'rb') as file: ftp.storbinary(f'STOR {file_path.name}', file)

