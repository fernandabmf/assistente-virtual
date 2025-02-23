import json
import os
import soundfile as sf
import numpy as np
import pyaudio
from transformers import pipeline
from difflib import SequenceMatcher

# Carregar modelo Wav2Vec2 para reconhecimento de fala
modelo_asr = pipeline("automatic-speech-recognition", model="jonatasgrosman/wav2vec2-large-xlsr-53-portuguese")

# Caminho do arquivo temporário para gravação
ARQUIVO_AUDIO = "comando.wav"

def carregar_comandos(caminho="C:/Users/nanda/OneDrive/Área de Trabalho/assistente_lojaDiscos/config.json"):
    with open(caminho, "r") as arquivo:
        return json.load(arquivo)

def gravar_audio(arquivo_audio, duracao=5, taxa_amostragem=16000, canais=1):
    #Grava áudio do microfone e salva no arquivo especificado.#
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=canais, rate=taxa_amostragem, input=True, frames_per_buffer=1024)

    print("Bem vindo(a) à loja de discos!")
    print("🎤 Ouvindo... Fale agora!")
    frames = [stream.read(1024) for _ in range(int(taxa_amostragem / 1024 * duracao))]

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Converter os bytes do áudio para array numpy e salvar como .wav
    audio_array = np.frombuffer(b''.join(frames), dtype=np.int16)
    sf.write(arquivo_audio, audio_array, taxa_amostragem)
    print("Áudio gravado com sucesso!")

def reconhecer_fala(arquivo_audio):
    #Processa o arquivo de áudio e converte para texto.#
    try:
        audio, samplerate = sf.read(arquivo_audio)
        resultado = modelo_asr(audio)
        print(f"Texto reconhecido: {resultado['text']}")
        return resultado["text"].lower()
    except Exception as e:
        return f"Erro ao processar áudio: {e}"

def processar_comando(fala, dados_comandos):
    #Compara a fala com os comandos disponíveis e retorna o mais similar.#
    maior_similaridade = 0
    comando_identificado = None

    for comando, dados in dados_comandos["comandos"].items():
        frase_comando = dados["frase"]
        similaridade = SequenceMatcher(None, fala, frase_comando).ratio()
        
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            comando_identificado = comando

    return comando_identificado if maior_similaridade > 0.75 else None

def executar_acao(comando, dados_comandos):
    #Executa a ação correspondente ao comando reconhecido.#
    if comando in dados_comandos:
        if comando in ["musica", "leds"]:
            estado = input(f"Digite 'ligar' ou 'desligar' para controlar {comando}: ").strip().lower()
            return dados_comandos[comando].get(f"acao_{estado}", "Comando inválido.")
        else:
            return dados_comandos[comando].get("acao", "Comando inválido.")
    return "Comando não encontrado."

def executar_assistente():
    #Executa o assistente, aguardando comandos de voz continuamente.
    comandos = carregar_comandos()
    
    while True:
        gravar_audio(ARQUIVO_AUDIO)  # Captura áudio do microfone
        fala = reconhecer_fala(ARQUIVO_AUDIO)
        
        if "sair" in fala:
            print("🔴 Encerrando o assistente.")
            break

        comando = processar_comando(fala, comandos)
        print(f"Comando identificado: {comando}")

        if comando:
            resultado = executar_acao(comando, comandos["comandos"])
            print(f"✅ Ação executada: {resultado}")
        else:
            print("⚠️ Comando não reconhecido. Tente novamente.")

if __name__ == "__main__":
    executar_assistente()
