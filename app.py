from flask import Flask, render_template, request, send_from_directory
from TTS.api import TTS
import os
os.makedirs ("static/audios", exist_ok=True)

app = Flask(__name__)

# Carga el modelo solo una vez
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# Asegura la carpeta de salida
os.makedirs("static/audios", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = request.form["texto"]
        nombre_archivo = "voz_lobo_generada.wav"
        ruta_salida = os.path.join("static", "audios", nombre_archivo)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ruta_muestra = os.path.join(BASE_DIR, "samples", "voz_sabio.wav")
        # Genera el audio con la voz clonada
        tts.tts_to_file(
            text=texto,
            file_path=ruta_salida,
            speaker_wav=ruta_muestra,
            language="es"
        )

        return render_template("index.html", audio=nombre_archivo)

    return render_template("index.html", audio=None)

# Ruta para servir el audio
@app.route("/static/audios/<path:filename>")
def download_file(filename):
    return send_from_directory("static/audios", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
