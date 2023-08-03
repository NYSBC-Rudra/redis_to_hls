import subprocess
import os
from imagestreamer import ImagetoVideoStreamer

os.chdir('live_server')
os.system('rm -r *.m3u8')
os.system('rm -r *.ts')
subprocess.Popen(['python3', '-m', 'http.server', '8000'])
os.chdir('..')
newstreamer = ImagetoVideoStreamer()
