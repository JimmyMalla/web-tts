from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write
import torch
import numpy as np

# Asegura que estás en modo CPU
device = "cpu"

# Carga el modelo y el procesador
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark").to(device)

# Texto a convertir y voz preestablecida
text = "Hola, la sabiduría del lobo se escucha en su silencio."
voice_preset = "v2/es_speaker_0"  # Usa esta para español

# Procesamiento
inputs = processor(text, voice_preset=voice_preset)
for k in inputs:
    inputs[k] = inputs[k].to(device)

# Generación de audio
audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()

# Normalizar y guardar audio como WAV
sample_rate = model.config.sample_rate
audio_array = (audio_array * 32767).astype(np.int16)
write("voz_lobo_bark.wav", sample_rate, audio_array)
