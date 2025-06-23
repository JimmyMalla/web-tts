from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav

texto = "La sabiduría no se impone. Se respira en el silencio del bosque."

# Genera audio
audio_array = generate_audio(texto, history_prompt="es_speaker_0")

# Guarda el archivo
write_wav("voz_lobo_bark.wav", SAMPLE_RATE, audio_array)
