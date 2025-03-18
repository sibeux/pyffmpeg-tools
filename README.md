# FFmpeg Python Tools

Kumpulan skrip Python berbasis **FFmpeg** untuk memproses video, seperti **trim, convert, dan manipulasi video lainnya** secara otomatis.

## 📌 Fitur

- Trim video berdasarkan jumlah part
- Konversi format video

## 🚀 Instalasi

Pastikan kamu telah menginstal **FFmpeg** dan **Python**.

1. **Instal FFmpeg** (jika belum terinstal):

   ```sh
   sudo apt install ffmpeg  # Ubuntu/Linux
   brew install ffmpeg      # macOS
   choco install ffmpeg     # Windows (via Chocolatey)
   ```

2. **Kloning repo ini & instal dependensi**:

   ```sh
   git clone https://github.com/sibeux/pyffmpeg-tools.git
   cd pyffmpeg-tools
   ```

## 🔧 Penggunaan

Contoh pemakaian untuk **trim video**:

```python
# Masukkan directory path input dan output video,
# lalu masukkan jumlah part yang diinginkan.

file_path = r"C:\Users\Nasrul Wahabi\Downloads\video.mp4".strip()
output_dir = r"C:\Users\Nasrul Wahabi\Downloads".strip()
num_parts = 2
```

---
**✨ Happy Coding!** 🚀
