# YT-DLP Automation

## 📌 Descrição

Automatizador de downloads do YouTube com:
- Download em áudio ou vídeo
- Organização automática por canal/data
- Barra de progresso
- Logs automáticos
- Painel de mídia interativo (PySide6 ou PySimpleGUI)
- Build `.exe` + instalador `.msi`

---

## ⚙️ Requisitos

- Python 3.8+
- pip
- ffmpeg no PATH
- `requirements.txt`:
    yt-dlp
    PySide6
    PySimpleGUI


---

## 🚀 Como usar

### 📥 Instalar dependências

```bash
pip install -r requirements.txt

Rodar CLI
    bash
        python yt_dlp_downloader.py

Rodar GUI
    bash
        python yt_dlp_downloader_gui.py

Gerar Executável
    bash
        pyinstaller --onefile yt_dlp_downloader.py
        pyinstaller --onefile --noconsole yt_dlp_downloader_gui.py


Criar Instalador
Use Inno Setup:

Edite installer.iss

Compile → .msi ou .exe instalador


Organização Automática
Arquivos organizados por Canal/Ano-Mes/Video.mp4

Logs salvos em yt_dlp_automation.log


Painel de Gerenciamento
Filtros por extensão, data, canal

Abrir, mover ou excluir

Interface PySide6 ou PySimpleGUI