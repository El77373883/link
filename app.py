import os
from flask import Flask, render_template, request, redirect
import yt_dlp

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/descargar')
def descargar():
    url = request.args.get('url')
    formato = request.args.get('tipo') # 'audio' o 'video'

    if not url:
        return "Falta la URL", 400

    # Configuración de yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best' if formato == 'audio' else 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraer info sin descargar al servidor
            info = ydl.extract_info(url, download=False)
            
            # Buscamos la URL directa del flujo de video/audio
            # Esto evita que el servidor se sature, el usuario descarga directo de la fuente
            download_url = info.get('url')
            
            if not download_url:
                # Si es un video complejo (ej. YouTube 1080p), tomamos el primer formato disponible
                formats = info.get('formats', [])
                download_url = formats[-1].get('url')

            return redirect(download_url)
    except Exception as e:
        return f"Error al procesar el enlace: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
