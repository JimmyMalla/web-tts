from flask import Flask, render_template, request, send_from_directory
import asyncio
import edge_tts
import os
import glob
from datetime import datetime

app = Flask(__name__)
os.makedirs("static/audios", exist_ok=True)

# Lista de voces en español (puedes expandirla con más opciones si deseas)
VOCES_ES = [
    "es-EC-LuisNeural", "es-ES-AlvaroNeural", "es-ES-ElviraNeural",
    "es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-US-AlonsoNeural",
    "es-US-PalomaNeural"
]

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    texto_generado = None
    voz_seleccionada = "es-EC-LuisNeural"

    if request.method == "POST":
        texto = request.form["texto"]
        voz = request.form.get("voz", voz_seleccionada)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"voz_{timestamp}.mp3"
        ruta_archivo = os.path.join("static", "audios", nombre_archivo)

        asyncio.run(generar_voz(texto, voz, ruta_archivo))
        limpiar_audios()  # Limpiar audios antiguos

        audio_file = nombre_archivo
        texto_generado = texto
        voz_seleccionada = voz

    # Historial de audios
    historial = sorted(
        glob.glob("static/audios/*.mp3"),
        key=os.path.getmtime,
        reverse=True
    )

    return render_template("index.html", audio_file=audio_file, texto=texto_generado, historial=historial, voces=VOCES_ES, voz_actual=voz_seleccionada)

@app.route("/static/audios/<path:filename>")
def descargar_audio(filename):
    return send_from_directory("static/audios", filename)

async def generar_voz(texto, voz, ruta_archivo):
    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate="-10%",
        pitch="-2Hz"
    )
    await communicate.save(ruta_archivo)

def limpiar_audios(max_audios=50):
    archivos = sorted(glob.glob("static/audios/*.mp3"), key=os.path.getmtime)
    while len(archivos) > max_audios:
        os.remove(archivos[0])
        archivos.pop(0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


