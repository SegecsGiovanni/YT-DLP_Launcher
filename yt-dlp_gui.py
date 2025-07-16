import os
import shutil
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from yt_dlp import YoutubeDL

# ====== CONFIGURAÇÕES ======

audio_folder = r'C:\Users\ADMIN\Music'
video_folder = r'C:\Users\ADMIN\Videos'

audio_exts = ['mp3', 'wav', 'wma', 'flac', 'aac', 'm4a', 'ogg']
video_exts = ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'mpg', 'mpeg']

os.makedirs(audio_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

# ====== FUNÇÃO PRINCIPAL ======

def baixar():
    url = url_entry.get()
    choice = choice_var.get()

    if not url:
        messagebox.showerror("Erro", "Cole o link do vídeo!")
        return

    def hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip().replace('%','')
            if percent:
                my_double_var.set(float(percent))
        elif d['status'] == 'finished':
            messagebox.showinfo("Download", "Concluído.")

    ydl_opts = {
        'restrictfilenames': True,
        'progress_hooks': [hook],
        # Removido o outtmpl que criava pastas por data. Fica para uma atualização futura.
        # Agora o vídeo será baixado no diretório atual
    }

    if choice == 1:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio',
            'merge_output_format': 'mp4'
        })
    elif choice == 2:
        ydl_opts.update({
            'format': 'bestaudio',
            'extract_audio': True,
            'audio_format': 'mp3'
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

    # Move arquivos baixados para as pastas definidas
    for file in os.listdir('.'):
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1][1:].lower()
            src_path = os.path.abspath(file)

            if ext in audio_exts:
                dest = os.path.join(audio_folder, file)
                shutil.move(src_path, dest)
            elif ext in video_exts:
                dest = os.path.join(video_folder, file)
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