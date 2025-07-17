import os
import subprocess

# Ganti ini ke path folder kamu (atau pakai os.getcwd() untuk folder saat ini)
folder_path = r"C:\Users\Nasrul Wahabi\Downloads\Compressed\KONOSUBA-OST\flac"

# Loop semua file dalam folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".m4a"):
        input_path = os.path.join(folder_path, filename)
        output_name = os.path.splitext(filename)[0] + ".flac"
        output_path = os.path.join(folder_path, output_name)

        print(f"Converting: {filename} → {output_name}")

        # Jalankan ffmpeg command
        result = subprocess.run([
            "ffmpeg", "-y", "-i", input_path, "-c:a", "flac", output_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"Success: {output_name}")
        else:
            print(f"Failed to convert: {filename}")
            print(result.stderr.decode())

print("Done.")
