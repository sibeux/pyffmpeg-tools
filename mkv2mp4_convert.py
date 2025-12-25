import os
import subprocess

from pathlib import Path


def convert_video(input_file, output_file):
    # Pastikan FFmpeg sudah diinstal
    try:
        subprocess.run(["ffmpeg", "-version"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("FFmpeg tidak ditemukan. Pastikan sudah diinstal dan ditambahkan ke PATH.")
        return
    print("Mengonversi file video ke format MP4...")

    # Buat output filename
    # Ambil nama file dari path lengkap
    filename = os.path.basename(input_file)
    # Ambil direktori dari path lengkap
    input_dir = os.path.dirname(input_file)
    print(f"Nama file: {filename}")
    # Ganti ekstensi dari MKV -> mp4
    output_name = os.path.splitext(filename)[0] + ".mp4"
    print(f"Output name: {output_name}")
    # Gabungkan direktori dan nama file mp4
    output_path = os.path.join(input_dir, output_name)
    print(f"Output path: {output_path}")

    # Konversi video
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-c", "copy",
        output_path
    ])
    print(f"Konversi selesai. File disimpan di: {output_file}")


# input path
input_path = str(input("Place your path here: "))
input_path = input_path.replace("\"", "")

input_file = rf"{input_path}"
output_file = Path(input_file).parent

if __name__ == "__main__":
    convert_video(input_file, output_file)
