from flask import Flask, render_template, request, send_from_directory, session, redirect
import asyncio
import edge_tts
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'voz_lobo_sabio_123'  # Necesario para usar session
os.makedirs("static/audios", exist_ok=True)

# Lista de voces en español disponibles
VOCES_ES = [
    "es-EC-LuisNeural", "es-AR-TomasNeural", "es-BO-MarceloNeural",
    "es-CL-LorenzoNeural", "es-CO-GonzaloNeural", "es-CR-JuanNeural",
    "es-CU-ManuelNeural", "es-DO-RamónNeural", "es-ES-AlvaroNeural",
    "es-GQ-JavierNeural", "es-GT-AndresNeural", "es-HN-CarlosNeural",
    "es-MX-JorgeNeural", "es-NI-JoseNeural", "es-PA-RobertoNeural",
    "es-PE-AlexNeural", "es-PR-GabrielNeural", "es-PY-MarioNeural",
    "es-SV-RodrigoNeural", "es-US-AlonsoNeural", "es-UY-MateoNeural",
    "es-VE-SebastianNeural"
]

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    texto_actual = ""
    voz_seleccionada = "es-EC-LuisNeural"

    if "historial" not in session:
        session["historial"] = []

    if request.method == "POST":
        texto_actual = request.form["texto"]
        voz_seleccionada = request.form["voz"]

        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"voz_{timestamp}.mp3"
        ruta_salida = os.path.join("static", "audios", nombre_archivo)

        # Ejecutar generación de voz
        asyncio.run(generar_voz(texto_actual, voz_seleccionada, ruta_salida))

        # Agregar al historial
        session["historial"].append({"texto": texto_actual, "archivo": nombre_archivo})
        session.modified = True

        audio_file = nombre_archivo

    return render_template("index.html",
                           audio_file=audio_file,
                           historial=session["historial"],
                           voces=VOCES_ES,
                           voz_actual=voz_seleccionada,
                           texto_actual=texto_actual)

@app.route("/static/audios/<path:filename>")
def descargar_audio(filename):
    return send_from_directory("static/audios", filename)

async def generar_voz(texto, voz, ruta_archivo):
    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate="-10%", pitch="-2Hz"
    )
    await communicate.save(ruta_archivo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



