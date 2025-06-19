from flask import Flask, render_template, request, send_from_directory
from TTS.api import TTS
import os
from datetime import datetime

app = Flask(__name__)

# Cargar el modelo español de Coqui
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = request.form["texto"]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo = f"voz_lobo_{timestamp}.wav"
        ruta_salida = os.path.join("static/audios", nombre_archivo)

        tts.tts_to_file(text=texto, file_path=ruta_salida)

        return render_template("index.html", audio_file=nombre_archivo)

    return render_template("index.html", audio_file=None)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("static/audios", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
