import json
import unicodedata
from pathlib import Path
from orientacao import Orientacao


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    @staticmethod
    def normalizar(texto):
        texto = unicodedata.normalize("NFD", str(texto).lower().strip())
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        for sinal in "?!.,;:()[]{}\\/\\-_":
            texto = texto.replace(sinal, " ")
        return " " + " ".join(texto.split()) + " "

    def carregar(self):
        try:
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("A base JSON precisa conter uma lista de orientações.")
            orientacoes = [Orientacao(item) for item in dados]
            if not orientacoes:
                raise ValueError("A base de conhecimento está vazia.")
            self.orientacoes = orientacoes
            return True
        except FileNotFoundError:
            print(f"Aviso: arquivo não encontrado: {self.caminho}")
        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as erro:
            print(f"Aviso: não foi possível carregar a base: {erro}")
        self.orientacoes = []
        return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = self.normalizar(pergunta)
        titulo_norm = self.normalizar(orientacao.titulo)
        pontos = 0
        for palavra_chave in orientacao.palavras_chave:
            chave = self.normalizar(palavra_chave).strip()
            if chave and f" {chave} " in pergunta_norm:
                pontos += 3
        palavras = set(pergunta_norm.split())
        palavras_titulo = set(titulo_norm.split())
        pontos += sum(1 for palavra in palavras if len(palavra) >= 4 and palavra in palavras_titulo)
        return pontos

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted(resultados, key=lambda item: item[0], reverse=True)
