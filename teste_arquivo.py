import torch
import torchaudio
from transformers import pipeline

# Carregar modelo Whisper
modelo = pipeline("automatic-speech-recognition", model="openai/whisper-small")

def reconhecer_fala(arquivo_audio):
    # Carregar áudio diretamente com torchaudio (sem ffmpeg)
    waveform, sample_rate = torchaudio.load(arquivo_audio)

    # Converter para texto
    resultado = modelo(waveform.numpy()[0])
    
    return resultado["text"]

# Teste com um arquivo de áudio
print(reconhecer_fala("audios/onde_estao_vinil.wav"))
