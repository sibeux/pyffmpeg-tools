import os

# Ganti ini dengan path folder kamu
folder_path = r"C:\Users\Nasrul Wahabi\Downloads\Video"

# Loop semua file di folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # Pastikan hanya file (bukan folder)
    if os.path.isfile(file_path):
        name, ext = os.path.splitext(filename)

        # Lewati kalau sudah .ts
        if ext.lower() == '.ts':
            continue

        new_filename = name + '.ts'
        new_file_path = os.path.join(folder_path, new_filename)

        # Cek apakah file tujuan sudah ada
        if os.path.exists(new_file_path):
            print(f"SKIPPED: {filename} -> {new_filename} (sudah ada)")
            continue

        # Ubah nama file
        os.rename(file_path, new_file_path)
        print(f"Renamed: {filename} -> {new_filename}")

print("Selesai mengganti ekstensi.")
