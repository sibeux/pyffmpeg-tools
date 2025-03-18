import os
import subprocess

def convert_video(input_file, output_file):
    """
    Mengonversi file video ke format MP4.
    
    Parameters:
        input_file (str): Path file input video.
        output_file (str): Path file output video (dengan ekstensi .mp4).
    """
    # Pastikan FFmpeg sudah diinstal
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("FFmpeg tidak ditemukan. Pastikan sudah diinstal dan ditambahkan ke PATH.")
        return
    
    print("Mengonversi file video ke format MP4...")
    
    # Konversi video
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-c:v", "copy",  # Salin video tanpa re-encoding
        "-c:a", "aac",   # Encode audio ke AAC
        "-y",            # Timpa file jika sudah ada
        output_file
    ])
    
    print(f"Konversi selesai. File disimpan di: {output_file}")

# Input pengguna
if __name__ == "__main__":
    input_file = r"C:\Users\Nasrul Wahabi\Downloads\Video\1.ts".strip()
    output_file = r"C:\Users\Nasrul Wahabi\Downloads\Video\1.mp4".strip()
    
    # Tambahkan ekstensi .mp4 jika belum ada
    if not output_file.endswith(".mp4"):
        output_file += ".mp4"
    
    convert_video(input_file, output_file)
