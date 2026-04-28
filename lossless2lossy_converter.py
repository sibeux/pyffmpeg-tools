import os
import subprocess

# Input path dari user
input_input = input("Place your path here: ").replace("\"", "")
folder_path = os.path.abspath(input_input)

# Pilih format output (Default Opus karena paling efisien)
# Bisa diganti ke "mp3" atau "m4a" (untuk AAC)
target_ext = "opus" 

# List ekstensi lossless yang ingin dideteksi
lossless_extensions = (".flac", ".wav", ".m4a")

# Buat folder output supaya file asli tidak tertumpuk
output_folder = os.path.join(folder_path, "converted_lossy")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print(f"Targeting: {target_ext.upper()} format")
print("-" * 30)

for filename in os.listdir(folder_path):
    if filename.lower().endswith(lossless_extensions):
        input_file = os.path.join(folder_path, filename)
        
        # Nama file output
        output_name = os.path.splitext(filename)[0] + f".{target_ext}"
        output_path = os.path.join(output_folder, output_name)

        print(f"Processing: {filename}...")

        # Command FFmpeg:
        # -ar 48000: Downsample ke 48kHz (optimal untuk telinga manusia)
        # -ac 2: Pastikan Stereo
        # -b:a 128k: Bitrate (128k Opus sudah setara 320k MP3)
        
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-ar", "48000",
            "-ac", "2"
        ]

        if target_ext == "opus":
            cmd += ["-c:a", "libopus", "-b:a", "128k", output_path]
        elif target_ext == "mp3":
            cmd += ["-c:a", "libmp3lame", "-q:a", "2", output_path] # -q:a 2 = VBR ~190-250kbps
        else:
            cmd += ["-b:a", "128k", output_path]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"Successfully converted to: {output_name}")
        else:
            print(f"Error converting {filename}")
            print(result.stderr.decode())

print("-" * 30)
print(f"Done! Check your files in: {output_folder}")