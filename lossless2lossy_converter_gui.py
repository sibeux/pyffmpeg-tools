import os
import subprocess
import threading
import tkinter as tk
from tkinter import scrolledtext

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lossless to Lossy Converter")
        self.root.geometry("600x500")
        
        # UI Elements
        # 1. Path Input
        path_frame = tk.Frame(root)
        path_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(path_frame, text="Path:").pack(side="left")
        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # 2. Paste Button
        self.paste_btn = tk.Button(path_frame, text="Paste", command=self.paste_path)
        self.paste_btn.pack(side="left")

        # 3. Indicator Frame (Red, Yellow, Green)
        ind_frame = tk.Frame(root)
        ind_frame.pack(pady=5)
        
        self.canvas = tk.Canvas(ind_frame, width=90, height=30)
        self.canvas.pack()
        
        self.red_light = self.canvas.create_oval(5, 5, 25, 25, fill="darkred")
        self.yellow_light = self.canvas.create_oval(35, 5, 55, 25, fill="darkgoldenrod")
        self.green_light = self.canvas.create_oval(65, 5, 85, 25, fill="darkgreen")

        self.set_indicator("red") # Initial state
        
        # 4. Run Button
        self.run_btn = tk.Button(root, text="Run", command=self.start_conversion, bg="green", fg="white", width=15)
        self.run_btn.pack(pady=5)
        
        # 5. Terminal Output
        self.terminal = scrolledtext.ScrolledText(root, width=80, height=20, bg="black", fg="white", font=("Consolas", 10))
        self.terminal.pack(pady=10, padx=10, fill="both", expand=True)

    def paste_path(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, clipboard_text.replace('"', ''))
        except tk.TclError:
            pass # Ignore if clipboard is empty or not string
            
    def set_indicator(self, state):
        self.root.after(0, self._set_indicator_safe, state)

    def _set_indicator_safe(self, state):
        self.canvas.itemconfig(self.red_light, fill="darkred")
        self.canvas.itemconfig(self.yellow_light, fill="darkgoldenrod")
        self.canvas.itemconfig(self.green_light, fill="darkgreen")
        
        if state == "red":
            self.canvas.itemconfig(self.red_light, fill="red")
        elif state == "yellow":
            self.canvas.itemconfig(self.yellow_light, fill="yellow")
        elif state == "green":
            self.canvas.itemconfig(self.green_light, fill="lime")

    def log(self, message):
        self.root.after(0, self._log_safe, str(message))

    def _log_safe(self, message):
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)

    def start_conversion(self):
        folder_path = self.path_entry.get().strip()
        if not folder_path:
            self.log("Error: Path is empty!")
            return
            
        if not os.path.exists(folder_path):
            self.log("Error: Path does not exist!")
            return

        self.set_indicator("yellow")
        self.run_btn.config(state="disabled")
        self.terminal.delete(1.0, tk.END) # Clear terminal for new run
        self.log(f"Starting conversion for directory: {folder_path}")
        
        # Run in separate thread so GUI doesn't freeze
        threading.Thread(target=self.process_conversion, args=(folder_path,), daemon=True).start()

    def process_conversion(self, folder_path):
        target_ext = "opus" 
        lossless_extensions = (".flac", ".wav", ".m4a")
        
        output_folder = os.path.join(folder_path, "flac")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        self.log(f"Targeting: {target_ext.upper()} format")
        self.log("-" * 30)

        success = True
        try:
            files_to_process = [f for f in os.listdir(folder_path) if f.lower().endswith(lossless_extensions)]
            
            if not files_to_process:
                self.log("No lossless files found in the directory.")
                self.set_indicator("green")
                self.root.after(0, lambda: self.run_btn.config(state="normal"))
                return
                
            for filename in files_to_process:
                input_file = os.path.join(folder_path, filename)
                output_name = os.path.splitext(filename)[0] + f".{target_ext}"
                output_path = os.path.join(output_folder, output_name)

                self.log(f"Processing: {filename}...")

                cmd = [
                    "ffmpeg", "-y", "-i", input_file,
                    "-ar", "48000",
                    "-ac", "2"
                ]

                if target_ext == "opus":
                    cmd += ["-c:a", "libopus", "-b:a", "128k", output_path]
                elif target_ext == "mp3":
                    cmd += ["-c:a", "libmp3lame", "-q:a", "2", output_path]
                else:
                    cmd += ["-b:a", "128k", output_path]

                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if result.returncode == 0:
                    self.log(f"Successfully converted to: {output_name}")
                else:
                    self.log(f"Error converting {filename}")
                    self.log(result.stderr.decode('utf-8', errors='ignore'))
                    success = False
            
            self.log("-" * 30)
            self.log(f"Done! Check your files in: {output_folder}")
            if success:
                self.set_indicator("green")
            else:
                self.set_indicator("red")
        except Exception as e:
            self.log(f"Exception occurred: {str(e)}")
            self.set_indicator("red")
        finally:
            self.root.after(0, lambda: self.run_btn.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()