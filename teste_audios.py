import unittest
from assistente_loja_discos import carregar_comandos, processar_comando, reconhecer_fala

class TestAssistente(unittest.TestCase):
    def setUp(self):
        self.comandos = carregar_comandos()

    def test_comando_disco_vinil(self):
        fala_vinil = "C:/Users/nanda/OneDrive/Área de Trabalho/assistente_lojaDiscos/audios/onde_estao_vinil.wav"
        transcricao = reconhecer_fala(fala_vinil)
        comando = processar_comando(transcricao, self.comandos)
        self.assertEqual(comando, "discos_vinil")

    def test_comando_cds(self):
        fala_cds = "C:/Users/nanda/OneDrive/Área de Trabalho/assistente_lojaDiscos/audios/onde_estao_cds.wav"
        transcricao = reconhecer_fala(fala_cds)
        comando = processar_comando(transcricao, self.comandos)
        self.assertEqual(comando, "cds")
        
    def test_comando_musica(self):
        fala_musica = "C:/Users/nanda/OneDrive/Área de Trabalho/assistente_lojaDiscos/audios/ligar_musica.wav"
        transcricao = reconhecer_fala(fala_musica)
        comando = processar_comando(transcricao, self.comandos)
        self.assertEqual(comando, "musica")

    def test_comando_leds(self):
        fala_leds = "C:/Users/nanda/OneDrive/Área de Trabalho/assistente_lojaDiscos/audios/ligar_leds.wav"
        transcricao = reconhecer_fala(fala_leds)
        comando = processar_comando(transcricao, self.comandos)
        self.assertEqual(comando, "leds")

    def test_comando_nao_reconhecido(self):
        fala = "comando inválido"
        comando = processar_comando(fala, self.comandos)
        self.assertIsNone(comando)

if __name__ == "__main__":
    unittest.main()
