import os
import subprocess

def get_video_duration(file_path):
    """
    Mendapatkan durasi video dalam detik menggunakan FFmpeg.
    
    Parameters:
        file_path (str): Path file video.
        
    Returns:
        float: Durasi video dalam detik.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout.strip())

def convert_and_split_ts_to_mp4(ts_file, output_dir, num_parts):
    """
    Mengonversi file .ts ke .mp4 dan membagi video menjadi beberapa bagian dengan durasi sama.
    
    Parameters:
        ts_file (str): Path file TS input.
        output_dir (str): Direktori output untuk file MP4.
        num_parts (int): Jumlah bagian yang ingin dibuat.
    """
    # Pastikan FFmpeg sudah diinstal
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("FFmpeg tidak ditemukan. Pastikan sudah diinstal dan ditambahkan ke PATH.")
        return
    
    # Buat direktori output jika belum ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Nama file output untuk keseluruhan video
    converted_file = os.path.join(output_dir, "converted.mp4")
    
    # Konversi file TS ke MP4
    print("Mengonversi file TS ke MP4...")
    subprocess.run([
        "ffmpeg",
        "-i", ts_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-y",
        converted_file
    ])
    
    print("Konversi selesai. Membagi video menjadi beberapa bagian...")
    
    # Dapatkan durasi video
    duration = get_video_duration(converted_file)
    part_duration = duration / num_parts  # Durasi setiap bagian
    
    # Potong video menjadi beberapa bagian
    for i in range(num_parts):
        start_time = i * part_duration
        output_file = os.path.join(output_dir, f"part_{i+1}.mp4")
        subprocess.run([
            "ffmpeg",
            "-i", converted_file,
            "-ss", str(start_time),
            "-t", str(part_duration),
            "-c", "copy",
            "-y",
            output_file
        ])
        print(f"Bagian {i+1} selesai: {output_file}")
    
    print("Semua bagian selesai diproses.")

# Input pengguna
if __name__ == "__main__":
    ts_file = r"C:\Users\Nasrul Wahabi\Documents\XuanZhi9\Pictures\Telegram\SIBEUX-SIBEUI\SIBEUX\1.mp4".strip()
    output_dir = r"C:\Users\Nasrul Wahabi\Documents\XuanZhi9\Pictures\Telegram\SIBEUX-SIBEUI\SIBEUX".strip()
    num_parts = 4
    
    convert_and_split_ts_to_mp4(ts_file, output_dir, num_parts)
