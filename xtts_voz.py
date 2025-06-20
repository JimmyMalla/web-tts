from TTS.api import TTS

# Carga el modelo XTTS v2
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

# Texto que quieres transformar en voz
texto = "El lobo no necesita demostrar su fuerza. Su silencio ya impone respeto."

# Genera la voz y guarda el audio
tts.tts_to_file(
    text=texto,
    file_path="static/audios/lobo_xtts.wav",
    speaker_wav="samples/xtts_voz.wav",  # Ruta a la muestra de voz
    language="es"
)
