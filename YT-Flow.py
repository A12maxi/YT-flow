import os
import subprocess
import sys
import threading
import urllib.request
import zipfile
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import re

# --- CONFIGURACIÓN DE RUTAS LOCALES ---
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta para el motor (FFmpeg)
RECURSOS_DIR = os.path.join(APP_DIR, "Archivos_YTFlow")
if not os.path.exists(RECURSOS_DIR):
    os.makedirs(RECURSOS_DIR)

# Carpeta para tus videos/música
ruta_destino = os.path.join(APP_DIR, "Descargas_YTFlow")
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

FFMPEG_BIN = os.path.join(RECURSOS_DIR, "ffmpeg.exe")
FFPROBE_BIN = os.path.join(RECURSOS_DIR, "ffprobe.exe")
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ICONO_PATH = resource_path("YT-Flow.png")
cancelar_descarga = False

# --- LÓGICA DE FUNCIONAMIENTO ---

def verificar_ffmpeg():
    return os.path.exists(FFMPEG_BIN) and os.path.exists(FFPROBE_BIN)

def progress_hook(d):
    global cancelar_descarga
    if cancelar_descarga: raise Exception("CANCELADO")
    if d['status'] == 'downloading':
        p_str = d.get('_percent_str', '0%')
        p_clean = re.sub(r'\x1b\[[0-9;]*m', '', p_str).replace('%','')
        try:
            p_float = float(p_clean)
            progress_var.set(p_float * 0.90) 
            status_var.set(f"Fluyendo: {p_float:.1f}%")
        except: pass
    elif d['status'] == 'finished':
        status_var.set("Finalizando archivo...")
        progress_var.set(95)
    root.update_idletasks()

def instalar_todo():
    try:
        from PIL import Image, ImageTk
        import yt_dlp
    except ImportError:
        status_var.set("Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "Pillow"])
        root.after(100, cargar_icono_pro)
    
    if not verificar_ffmpeg():
        status_var.set("Configurando motor de video...")
        zip_path = os.path.join(RECURSOS_DIR, "temp.zip")
        try:
            urllib.request.urlretrieve(FFMPEG_URL, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith("ffmpeg.exe") or file.endswith("ffprobe.exe"):
                        fname = os.path.basename(file)
                        with zip_ref.open(file) as s, open(os.path.join(RECURSOS_DIR, fname), "wb") as t:
                            t.write(s.read())
            os.remove(zip_path)
        except:
            status_var.set("Error. Intenta ejecutar como Administrador.")
            return
    status_var.set("YT-Flow Listo.")

def cargar_icono_pro():
    if not os.path.exists(ICONO_PATH): return
    try:
        from PIL import Image, ImageTk
        img = Image.open(ICONO_PATH).resize((32, 32), Image.Resampling.LANCZOS)
        global photo_icon
        photo_icon = ImageTk.PhotoImage(img)
        root.iconphoto(False, photo_icon)
    except: pass

def hilo_descarga(url, modo):
    global cancelar_descarga, ruta_destino
    import yt_dlp
    cancelar_descarga = False
    
    # OPCIONES PARA SOLUCIONAR EL ERROR DE FFPROBE
    ydl_opts = {
        'ffmpeg_location': RECURSOS_DIR, # RUTA DIRECTA AL MOTOR
        'outtmpl': os.path.join(ruta_destino, "%(title)s.%(ext)s"),
        'progress_hooks': [progress_hook],
        'quiet': True,
    }

    if modo == "Audio (MP3)":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if not cancelar_descarga:
            progress_var.set(100)
            status_var.set("¡Completado!")
            messagebox.showinfo("YT-Flow", "Guardado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Fallo al procesar: {e}")
    finally:
        btn_descargar.config(state="normal")
        btn_cancelar.config(state="disabled")

def iniciar_descarga():
    url = entry_url.get()
    modo = combo_modo.get()
    if not url: return
    btn_descargar.config(state="disabled")
    btn_cancelar.config(state="normal")
    threading.Thread(target=hilo_descarga, args=(url, modo), daemon=True).start()

# --- INTERFAZ ---
root = tk.Tk()
root.title("YT-Flow - Video Downloader")
root.geometry("550x580")
root.after(10, cargar_icono_pro)

style = ttk.Style()
style.configure("Big.TButton", font=("Arial", 11, "bold"))

progress_var = tk.DoubleVar()
status_var = tk.StringVar(value="Iniciando...")

frame = ttk.Frame(root, padding="25")
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Enlace de YouTube:", font=("Arial", 10, "bold")).pack(pady=5)
entry_url = ttk.Entry(frame, width=60)
entry_url.pack(pady=5)

ttk.Label(frame, text="Formato de descarga:", font=("Arial", 10)).pack(pady=(10, 0))
combo_modo = ttk.Combobox(frame, values=["Video (MP4)", "Audio (MP3)"], state="readonly")
combo_modo.current(0)
combo_modo.pack(pady=5)

btn_descargar = ttk.Button(frame, text="DESCARGAR VIDEO", style="Big.TButton", command=iniciar_descarga)
btn_descargar.pack(pady=(25, 5), fill="x", ipady=15)

btn_cancelar = ttk.Button(frame, text="CANCELAR Y BORRAR", style="Big.TButton", state="disabled")
btn_cancelar.pack(pady=5, fill="x", ipady=10)

ttk.Label(frame, textvariable=status_var).pack(pady=15)
progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100, length=450)
progress_bar.pack(pady=10)

root.after(500, lambda: threading.Thread(target=instalar_todo, daemon=True).start())
root.mainloop()