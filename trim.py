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

def split_video(file_path, output_dir, num_parts):
    """
    Membagi video menjadi beberapa bagian dengan durasi sama.
    
    Parameters yang dipakai:
        file_path (str): Path file video input.
        output_dir (str): Direktori output untuk file hasil potongan.
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

    print("Membagi video menjadi beberapa bagian...")
    
    # Dapatkan durasi video
    duration = get_video_duration(file_path)
    part_duration = duration / num_parts  # Durasi setiap bagian
    
    # Potong video menjadi beberapa bagian
    for i in range(num_parts):
        start_time = i * part_duration
        output_file = os.path.join(output_dir, f"part_{i+1}.mp4")
        subprocess.run([
            "ffmpeg",
            "-i", file_path,
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
    file_path = r"C:\Users\Nasrul Wahabi\Downloads\Compressed\A-19\A-19.mp4".strip()
    output_dir = r"C:\Users\Nasrul Wahabi\Downloads\Compressed\A-19".strip()
    num_parts = 3
    
    split_video(file_path, output_dir, num_parts)
