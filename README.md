# YT-Flow 🚀 - Video & Audio Downloader

**YT-Flow** es una herramienta ligera y portátil diseñada para descargar vídeos y audio de YouTube de forma sencilla, organizada y rápida. El programa está optimizado para funcionar sin instalación (Portable), manteniendo todos sus archivos y descargas en una carpeta local para no ensuciar el sistema.


## ✨ Características Principales

* **🎬 Descarga de Video:** Baja vídeos en formato MP4 con la mejor calidad disponible (hasta 1080p/4K dependiendo del origen).
* **🎵 Descarga de Audio:** Extrae el audio de cualquier vídeo y lo convierte automáticamente a MP3 (192kbps).
* **📦 100% Portable:** Crea sus propias carpetas (`Archivos_YTFlow` y `Descargas_YTFlow`) al lado del ejecutable. No requiere instalación de drivers en Windows.
* **🛠️ Autoreparable:** Si no detecta el motor de procesado (FFmpeg), el programa intenta configurarlo automáticamente.
* **📊 Interfaz Intuitiva:** Barra de progreso en tiempo real y selector de formato (Video/Audio).

## 🚀 Cómo funciona

El programa utiliza tres pilares tecnológicos:
1.  **Python + Tkinter:** Para una interfaz gráfica rápida y funcional.
2.  **yt-dlp:** El motor más avanzado actualmente para la extracción de metadatos y enlaces de descarga de vídeo.
3.  **FFmpeg:** Utilizado para el post-procesamiento (unir vídeo y audio de alta calidad o convertir a MP3).

### Estructura de Carpetas
Al ejecutarlo, el programa organiza todo de la siguiente manera:
- `YT-Flow.exe`: El programa principal.
- `Archivos_YTFlow/`: Contiene el motor FFmpeg necesario para que las descargas no fallen.
- `Descargas_YTFlow/`: Carpeta donde se guardarán todos tus archivos descargados.

## 🛠️ Instalación y Uso

1.  Descarga el ejecutable desde la sección de [Releases].
2.  Coloca el archivo en la carpeta donde quieras que se guarden tus descargas.
3.  Pega el enlace de YouTube, elige si quieres Video o Audio y pulsa **Descargar**.

> **Nota:** La primera vez que lo uses, el programa configurará el motor de vídeo. Ten paciencia mientras se completa la barra de "Configurando motor".

## ⚠️ Descargo de Responsabilidad (Disclaimer)

Este software ha sido creado exclusivamente con fines **educativos y de uso personal**. El desarrollador no se hace responsable del uso indebido de esta herramienta. Por favor, respeta los derechos de autor de los creadores de contenido y los Términos de Servicio de las plataformas originales. No utilices este programa para descargar contenido protegido sin el permiso del propietario.

---
Creado con ❤️ por A12maxi
