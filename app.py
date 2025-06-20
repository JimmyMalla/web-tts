from flask import Flask, render_template, request, send_from_directory
from TTS.api import TTS
import os

app = Flask(__name__)

# Crea carpetas si no existen
os.makedirs("static/audios", exist_ok=True)

# Carga el modelo
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None

    if request.method == "POST":
        texto = request.form["texto"]
        nombre_archivo = "voz_lobo_generada.wav"
        ruta_salida = os.path.join("static", "audios", nombre_archivo)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ruta_muestra = os.path.join(BASE_DIR, "samples", "voz_sabio.wav")

        # Verifica que el archivo existe
        if not os.path.isfile(ruta_muestra):
            return f"❌ Error: El archivo de muestra no se encontró en: {ruta_muestra}"

        try:
            # Genera el audio clonando la voz
            tts.tts_to_file(
                text=texto,
                speaker_wav=ruta_muestra,
                language="es",
                file_path=ruta_salida
            )
            audio_file = nombre_archivo
        except Exception as e:
            return f"❌ Error al generar el audio: {e}"

    return render_template("index.html", audio_file=audio_file)

@app.route("/static/audios/<path:filename>")
def download_file(filename):
    return send_from_directory("static/audios", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

