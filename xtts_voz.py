from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

tts.tts_to_file(
    text="Hola, soy la voz del lobo sabio.",
    speaker_wav="samples/voz_sabio.wav",
    language="es",
    file_path="voz_prueba.wav"
)
