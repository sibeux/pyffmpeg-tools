import os
import subprocess
from natsort import natsorted

folder = r"C:\Users\Nasrul Wahabi\Downloads\Video\2. What is React.js And Why Would You Use It⁇"

# Ambil semua file mp4 dan urutkan secara natural
files = natsorted([f for f in os.listdir(folder) if f.endswith('.mp4')])

# Buat file concat.txt
with open('concat.txt', 'w', encoding='utf-8') as f:
    for file in files:
        full_path = os.path.join(folder, file).replace("\\", "/")
        f.write(f"file '{full_path}'\n")

# Jalankan ffmpeg
subprocess.run([
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'concat.txt',
    '-c', 'copy',
    'output.mp4'
])