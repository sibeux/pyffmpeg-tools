import os
import subprocess


def get_video_duration(file_path):
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
    try:
        subprocess.run(["ffmpeg", "-version"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("FFmpeg tidak ditemukan. Pastikan sudah diinstal dan ditambahkan ke PATH.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Membagi video menjadi beberapa bagian...")

    duration = get_video_duration(file_path)
    part_duration = duration / num_parts

    for i in range(num_parts):
        start_time = i * part_duration
        output_file = os.path.join(output_dir, f"part_{i+1}.mp4")
        subprocess.run([
            "ffmpeg",
            "-ss", str(start_time),
            "-i", file_path,
            "-t", str(part_duration),
            "-c:v", "libx264", "-c:a", "aac",  # encode ulang agar stabil
            "-preset", "fast",                 # opsional: lebih cepat
            "-y",
            output_file
        ])
        print(f"Bagian {i+1} selesai: {output_file}")

    print("Semua bagian selesai diproses.")


if __name__ == "__main__":
    file_path = r"C:\Users\Nasrul Wahabi\Documents\XuanZhi9\Pictures\Telegram\SIBEUX-SIBEUI\SIBEUX\A-24\A-24.mkv".strip()
    output_dir = r"C:\Users\Nasrul Wahabi\Documents\XuanZhi9\Pictures\Telegram\SIBEUX-SIBEUI\SIBEUX\A-24".strip()
    num_parts = 2

    split_video(file_path, output_dir, num_parts)
