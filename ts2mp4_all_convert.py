import os
import subprocess

def convert_video(input_file, output_file):
    """Mengonversi file video dari TS ke MP4 menggunakan FFmpeg."""
    try:
        subprocess.run(["ffmpeg", "-version"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ FFmpeg tidak ditemukan. Pastikan sudah diinstal dan ditambahkan ke PATH.")
        return

    # Konversi video
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-c:v", "copy",  # salin video tanpa re-encoding
        "-c:a", "aac",   # encode audio ke AAC
        "-y",            # timpa jika file .mp4 sudah ada
        output_file
    ])


def convert_all_ts_to_mp4(folder_path):
    """Mencari dan mengonversi semua file .ts dalam folder menjadi .mp4"""
    files = os.listdir(folder_path)
    ts_files = [f for f in files if f.lower().endswith(".ts")]

    if not ts_files:
        print("Tidak ada file .ts ditemukan di folder.")
        return

    print(f"🔄 Menemukan {len(ts_files)} file .ts. Memulai konversi...")

    for i, ts_file in enumerate(ts_files, 1):
        input_path = os.path.join(folder_path, ts_file)
        mp4_name = os.path.splitext(ts_file)[0] + ".mp4"
        output_path = os.path.join(folder_path, mp4_name)

        print(f"[{i}/{len(ts_files)}] 🎞️ {ts_file} -> {mp4_name}")
        convert_video(input_path, output_path)

    print("\n✅ Semua file selesai dikonversi.")


if __name__ == "__main__":
    folder_path = r"C:\Users\Nasrul Wahabi\Downloads\Video".strip()
    convert_all_ts_to_mp4(folder_path)
