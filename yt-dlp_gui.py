import os
import shutil
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from yt_dlp import YoutubeDL
import re
from pathlib import Path
from platformdirs import user_download_dir, user_video_dir

# ====== CONFIGURAÇÕES ======

audio_folder = Path(user_download_dir())
video_folder = Path(user_video_dir())

audio_exts = ['mp3', 'wav', 'wma', 'flac', 'aac', 'm4a', 'ogg']
video_exts = ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'mpg', 'mpeg']

audio_folder.mkdir(parents=True, exist_ok=True)
video_folder.mkdir(parents=True, exist_ok=True)

# ====== FUNÇÃO PARA LIMPAR PERCENTUAL E REMOVER ANSI ======

def limpar_percent(s):
    s = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', s)  # remove ANSI
    s = s.strip().replace('%', '')
    match = re.search(r'(\d+(\.\d+)?)', s)  # captura número com ou sem decimal
    return match.group(1) if match else '0.0'

# ====== FUNÇÃO PRINCIPAL ======

def baixar():
    url = url_entry.get()
    choice = choice_var.get()

    if not url:
        messagebox.showerror("Erro", "Cole o link do vídeo!")
        return

    def hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                percent = downloaded / total * 100
                my_double_var.set(percent)
                print(f"[DEBUG] Percent calculado: {percent:.2f}")
            else:
                my_double_var.set(0)
                print("[DEBUG] Total desconhecido, barra zerada.")
        elif d['status'] == 'finished':
            messagebox.showinfo("Download", "Concluído.")

    ydl_opts = {
        'ignoreconfig': True,
        'restrictfilenames': True,
        'progress_hooks': [hook],
    }

    if choice == 1:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio',
            'merge_output_format': 'mp4',
            'outtmpl': str(video_folder / '%(title)s.%(ext)s')
        })
    elif choice == 2:
        ydl_opts.update({
            'format': 'bestaudio',
            'extract_audio': True,
            'audio_format': 'mp3',
            'outtmpl': str(audio_folder / '%(title)s.%(ext)s')
        })
    else:
        messagebox.showerror("Erro", "Selecione o tipo de download.")
        return

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return

    # Move arquivos baixados para as pastas definidas (extra safety)
    for file in os.listdir('.'):
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1][1:].lower()
            src_path = os.path.abspath(file)

            if ext in audio_exts:
                dest = audio_folder / file
                if not dest.exists():
                    shutil.move(src_path, dest)
                else:
                    base, extension = os.path.splitext(file)
                    counter = 1
                    while (audio_folder / f"{base}_{counter}{extension}").exists():
                        counter += 1
                    dest = audio_folder / f"{base}_{counter}{extension}"
                    shutil.move(src_path, dest)
            elif ext in video_exts:
                dest = video_folder / file
                if not dest.exists():
                    shutil.move(src_path, dest)
                else:
                    base, extension = os.path.splitext(file)
                    counter = 1
                    while (video_folder / f"{base}_{counter}{extension}").exists():
                        counter += 1
                    dest = video_folder / f"{base}_{counter}{extension}"
                    shutil.move(src_path, dest)

    messagebox.showinfo("Finalizado", "Download e organização concluídos.")

# ====== INTERFACE GRÁFICA ======

root = tk.Tk()
root.title("YT-DLP Downloader")

tk.Label(root, text="Cole aqui o link do vídeo:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

choice_var = tk.IntVar()

tk.Radiobutton(root, text="Vídeo em máxima qualidade", variable=choice_var, value=1).pack(anchor="w")
tk.Radiobutton(root, text="Apenas áudio (MP3)", variable=choice_var, value=2).pack(anchor="w")

my_double_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=my_double_var, maximum=100)
progress_bar.pack(fill="x", padx=10, pady=10)

def start_download_thread():
    t = threading.Thread(target=baixar)
    t.start()

tk.Button(root, text="Baixar", command=start_download_thread).pack(pady=10)

root.mainloop()