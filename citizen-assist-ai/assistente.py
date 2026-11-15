import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.pasta_dados = Path("data")
        self.arquivo_historico = self.pasta_dados / "historico.json"
        self.arquivo_csv = self.pasta_dados / "atendimentos.csv"
        self.pasta_dados.mkdir(exist_ok=True)
        self._carregar_historico()

    def _carregar_historico(self):
        try:
            with self.arquivo_historico.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.historico = dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            self.historico = []

    @staticmethod
    def _tem_dado_pessoal(texto):
        return "@" in texto or sum(caractere.isdigit() for caractere in texto) >= 8

    @staticmethod
    def _confirmar_ajuda():
        while True:
            resposta = input("Essa orientação respondeu sua dúvida? (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Entrada inválida. Digite apenas s ou n.")

    def _registrar(self, origem, pergunta, orientacao_id, encontrou, ajudou,
                   tentativas, inicio):
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao_id,
            "encontrou": bool(encontrou),
            "ajudou": bool(ajudou),
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1)
        }
        self.historico.append(registro)
        with self.arquivo_historico.open("w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

    def perguntar(self):
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if not pergunta:
                print("Digite uma dúvida ou 0 para voltar.")
                continue
            if self._tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone, e-mail ou outros dados pessoais. Reescreva.")
                continue

            inicio = time.time()
            tentativas = 1
            resultados = self.base.buscar(pergunta)
            pontos, melhor = resultados[0]
            if pontos < 3:
                print("Não encontrei uma orientação com confiança suficiente.")
                print("Tente outras palavras ou navegue pelas categorias.")
                self._registrar("pergunta", pergunta, None, False, False, tentativas, inicio)
                continue

            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir(pontos)
            for pontos_alt, alternativa in resultados[1:3]:
                if pontos_alt >= 3:
                    print(f"\nAlternativa ({pontos_alt} pontos): {alternativa.titulo} [{alternativa.categoria}]")
            ajudou = self._confirmar_ajuda()
            self._registrar("pergunta", pergunta, melhor.id, True, ajudou, tentativas, inicio)

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return
        while True:
            print("\n=== CATEGORIAS ===")
            for indice, categoria in enumerate(categorias, 1):
                print(f"{indice}. {categoria}")
            print("0. Voltar")
            escolha = input("Escolha uma categoria: ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(categorias)):
                print("Opção inválida. Tente novamente.")
                continue
            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f"\n=== {categoria.upper()} ===")
                for indice, orientacao in enumerate(orientacoes, 1):
                    print(f"{indice}. {orientacao.titulo}")
                print("0. Voltar")
                item = input("Escolha uma orientação: ").strip()
                if item == "0":
                    break
                if not item.isdigit() or not (1 <= int(item) <= len(orientacoes)):
                    print("Opção inválida. Tente novamente.")
                    continue
                inicio = time.time()
                orientacao = orientacoes[int(item) - 1]
                orientacao.exibir()
                ajudou = self._confirmar_ajuda()
                self._registrar("categoria", orientacao.titulo, orientacao.id,
                                True, ajudou, 1, inicio)

    def indicadores(self):
        atendimentos = [h for h in self.historico if h.get("origem") != "avaliacao"]
        total = len(atendimentos)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return
        encontrados = sum(1 for h in atendimentos if h["encontrou"])
        ajudaram = sum(1 for h in atendimentos if h["ajudou"])
        tempo = sum(h["tempo_segundos"] for h in atendimentos) / total
        tentativas = sum(h["tentativas"] for h in atendimentos) / total
        sem_solucao = [h["pergunta"] for h in atendimentos if not h["ajudou"]]
        facilidade = [h["facilidade"] for h in self.historico if "facilidade" in h]
        print("\n=== INDICADORES ===")
        print(f"Atendimentos registrados: {total}")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}%")
        print(f"Tempo médio por atendimento: {tempo:.1f} segundos")
        print(f"Tentativas por atendimento: {tentativas:.1f}")
        print("Facilidade de uso (1 a 5):", f"{sum(facilidade) / len(facilidade):.1f}" if facilidade else "ainda não avaliada")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(" -", duvida)
        else:
            print(" - Nenhuma registrada.")

    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos"]
        with self.arquivo_csv.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(h for h in self.historico if h.get("origem") != "avaliacao")
        print(f"Atendimentos exportados para: {self.arquivo_csv}")

    def avaliar_facilidade(self):
        while True:
            nota = input("\nDe 1 a 5, quão fácil foi usar o assistente? ").strip()
            if nota.isdigit() and 1 <= int(nota) <= 5:
                self.historico.append({"data": datetime.now().isoformat(timespec="seconds"),
                                       "origem": "avaliacao", "pergunta": "",
                                       "id_orientacao": None, "encontrou": False,
                                       "ajudou": False, "tentativas": 0,
                                       "tempo_segundos": 0.0, "facilidade": int(nota)})
                with self.arquivo_historico.open("w", encoding="utf-8") as arquivo:
                    json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)
                return
            print("Nota inválida. Digite um número de 1 a 5.")

    def executar(self):
        while True:
            print(f"\n===== {self.nome} =====")
            print("1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Ver indicadores")
            print("4. Exportar atendimentos para CSV")
            print("0. Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                self.perguntar()
            elif opcao == "2":
                self.navegar()
            elif opcao == "3":
                self.indicadores()
            elif opcao == "4":
                self.exportar_csv()
            elif opcao == "0":
                self.avaliar_facilidade()
                self.exportar_csv()
                self.indicadores()
                print("Obrigado por utilizar o Citizen Assist AI!")
                break
            else:
                print("Opção inválida. Digite uma opção do menu.")
