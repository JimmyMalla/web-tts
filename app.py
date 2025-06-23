from flask import Flask, render_template, request, send_from_directory
import asyncio
import edge_tts
import os

app = Flask(__name__)

# Aseguramos que la carpeta de audios exista
os.makedirs("static/audios", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None

    if request.method == "POST":
        texto = request.form["texto"]
        nombre_archivo = "voz_lobo_edge.mp3"
        ruta_salida = os.path.join("static", "audios", nombre_archivo)

        # Ejecutamos edge-tts
        asyncio.run(generar_voz(texto, ruta_salida))

        audio_file = nombre_archivo

    return render_template("index.html", audio_file=audio_file)


@app.route("/static/audios/<path:filename>")
def descargar_audio(filename):
    return send_from_directory("static/audios", filename)


async def generar_voz(texto, ruta_archivo):
    communicate = edge_tts.Communicate(
        text=texto,
        voice="es-MX-JorgeNeural",  # Puedes cambiar la voz aquí
        rate="-10%",
        pitch="-2Hz"
    )
    await communicate.save(ruta_archivo)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


