import os
import shutil
from yt_dlp import YoutubeDL

# Pastas raiz de destino
audio_folder = r'C:\Users\ADMIN\Music'
video_folder = r'C:\Users\ADMIN\Videos'

# Cria pastas se nao existirem
os.makedirs(audio_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

# Extensões para detectar tipo
audio_exts = ['mp3', 'wav', 'wma', 'flac', 'aac', 'm4a', 'ogg']
video_exts = ['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'mpg', 'mpeg']

print("="*40)
print("       YT-DLP Downloader Python")
print("="*40)

url = input("\nCole aqui o link do video: ")

print("\nO que voce deseja baixar?")
print("1 - Video em maxima qualidade")
print("2 - Apenas o audio (MP3)")
choice = input("Escolha [1 ou 2]: ")

def hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        print(f"\rProgresso: {percent}", end='')
    elif d['status'] == 'finished':
        print("\nDownload concluido.")

# Config base
ydl_opts = {
    'restrictfilenames': True,
    'progress_hooks': [hook],
    'outtmpl': '%(uploader)s/%(upload_date>%Y-%m)/%(title)s.%(ext)s'
}

# Ajusta conforme escolha
if choice == '1':
    ydl_opts.update({
        'format': 'bestvideo+bestaudio',
        'merge_output_format': 'mp4'
    })
elif choice == '2':
    ydl_opts.update({
        'format': 'bestaudio',
        'extract_audio': True,
        'audio_format': 'mp3'
    })
else:
    print("\nOpcao invalida. Finalizando script.")
    exit()

# Executa download
with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# Move o diretório inteiro para destino final

# Como criamos subpastas por canal/data, vamos mover cada pasta gerada

for folder in os.listdir('.'):
    if os.path.isdir(folder):
        # Detecta se há arquivos de audio ou video dentro
        moved = False
        for root, dirs, files in os.walk(folder):
            for f in files:
                ext = os.path.splitext(f)[1][1:].lower()
                src_path = os.path.join(root, f)
                if ext in audio_exts:
                    dest = os.path.join(audio_folder, folder)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(src_path, dest)
                    moved = True
                elif ext in video_exts:
                    dest = os.path.join(video_folder, folder)
                    os.makedirs(dest, exist_ok=True)
                    shutil.move(src_path, dest)
                    moved = True
        if moved:
            # Remove pasta vazia
            shutil.rmtree(folder)

print("\nOrganizacao concluida.")