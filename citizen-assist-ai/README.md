# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

## 1\. Projeto

O Citizen Assist AI é um assistente executado no terminal que ajuda jovens que estão ingressando no mercado de trabalho a encontrar orientações básicas sobre documentação pessoal, trabalho e emprego e serviços digitais do governo.

**Problema:** informações sobre documentos, contratação, direitos e serviços públicos estão distribuídas em diferentes portais. O projeto reúne orientações introdutórias, indica a fonte oficial e informa a data de verificação.

**Público atendido:** jovens em busca do primeiro emprego ou de informações para iniciar sua vida profissional.

**ODS relacionados:**

- ODS 4 — Educação de qualidade: apoio ao acesso à informação e à qualificação profissional.  
- ODS 8 — Trabalho decente e crescimento econômico: orientação introdutória sobre ingresso no mercado de trabalho e direitos.  
- ODS 10 — Redução das desigualdades: organização de informações públicas em linguagem simples.  
- ODS 16 — Paz, justiça e instituições eficazes: incentivo ao uso de fontes públicas oficiais.

## 2\. Estrutura do projeto

```
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

`historico.json` e `atendimentos.csv` são criados/atualizados pelo programa durante a execução.

## 3\. Como executar

1. Instale o Python 3.10 ou superior.  
2. Baixe ou clone este repositório.  
3. Abra o terminal na pasta `citizen-assist-ai`.  
4. Execute:

```sh
python main.py
```

Não são necessárias bibliotecas externas. O projeto utiliza módulos da biblioteca padrão do Python.

## 4\. Organização em classes

- **Orientacao:** representa um registro do JSON. Guarda os atributos da orientação e possui o método `exibir()`.  
- **BaseConhecimento:** carrega o JSON, cria objetos `Orientacao`, lista categorias, filtra orientações e realiza a busca pontuada.  
- **Assistente:** controla o menu e o atendimento, registra o histórico, calcula indicadores e exporta o CSV.

A composição ocorre porque o objeto `Assistente` recebe e mantém um objeto `BaseConhecimento`, que por sua vez mantém uma lista de objetos `Orientacao`.

## 5\. Regra de pontuação da busca

A pergunta, o título e as palavras-chave são normalizados: letras minúsculas, sem acentos e sem pontuação.

- Cada palavra-chave encontrada na pergunta: **\+3 pontos**.  
- Cada palavra da pergunta com pelo menos quatro letras que também aparece no título: **\+1 ponto**.  
- **Confiança alta:** 6 pontos ou mais.  
- **Confiança média:** de 3 a 5 pontos.  
- **Sem resultado:** menos de 3 pontos.

A busca devolve uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação. A tela apresenta o melhor resultado e até duas alternativas com pelo menos 3 pontos.

## 6\. Privacidade, transparência e tratamento de erros

- O assistente não solicita nome, CPF, telefone ou e-mail.  
- Perguntas contendo `@` ou uma sequência de oito ou mais dígitos são recusadas e não entram no histórico.  
- Entradas vazias, opções fora da faixa e respostas diferentes de `s/n` são tratadas sem encerrar o programa.  
- A navegação por categorias possui opção `0` para voltar em cada tela.  
- As respostas mostram fonte, data de verificação e o aviso: **“este assistente NÃO é um canal oficial.”**  
- Arquivo JSON ausente, vazio, inválido ou corrompido é tratado com mensagem de aviso, sem traceback para o usuário.

## 7\. Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` com data, origem, pergunta, id da orientação, indicação de resultado, indicação de ajuda, tentativas e tempo em segundos. Ao sair, o usuário informa uma nota de facilidade de 1 a 5\. O CSV é exportado com `csv.DictWriter` para `data/atendimentos.csv`.

O menu permite consultar percentual de respostas encontradas, taxa de atendimentos que ajudaram, tempo médio, tentativas médias, facilidade média registrada e dúvidas sem solução.

## 8\. Fontes consultadas

As orientações foram construídas a partir de páginas oficiais. A data registrada no JSON indica a conferência realizada para esta versão do projeto; as regras podem mudar e devem ser verificadas novamente antes de uma decisão individual.

- Carteira de Trabalho Digital: [https\://www\.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho](https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho)  
- Conta gov.br: [https\://www\.gov.br/pt-br/servicos/criar-sua-conta-gov.br](https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br)  
- Receita Federal — Serviços: [https\://servicos.receitafederal.gov.br/](https://servicos.receitafederal.gov.br/)  
- Carteira de Identidade Nacional: [https\://www\.gov.br/pt-br/servicos/obter-carteira-de-identidade-nacional](https://www.gov.br/pt-br/servicos/obter-carteira-de-identidade-nacional)  
- Aprendizagem profissional — MTE: [https\://www\.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2026/julho/aprendizagem-profissional-regras-direitos-e-funcionamento-do-contrato-de-aprendizagem](https://www.gov.br/trabalho-e-emprego/pt-br/noticias-e-conteudo/2026/julho/aprendizagem-profissional-regras-direitos-e-funcionamento-do-contrato-de-aprendizagem)  
- Seguro-desemprego: [https\://www\.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego](https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego)  
- Extrato do FGTS — CAIXA: [https\://www\.caixa.gov.br/beneficios-trabalhador/fgts/extrato-FGTS/Paginas/default.aspx](https://www.caixa.gov.br/beneficios-trabalhador/fgts/extrato-FGTS/Paginas/default.aspx)  
- Combate ao trabalho infantil — MTE: [https\://www\.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/Combate-trabalho-infantil/erradicacao-do-trabalho-infantil](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/areas-de-atuacao/Combate-trabalho-infantil/erradicacao-do-trabalho-infantil)  
- Aplicativo FGTS: [https\://www\.fgts.gov.br/Paginas/trabalhador/app-fgts.aspx](https://www.fgts.gov.br/Paginas/trabalhador/app-fgts.aspx)

## 9\. Teste com usuários

| Indicador | Resultado real |
| :---- | :---- |
| Pessoas participantes  | \- |
| Total de atendimentos | \- |
| Respostas encontradas (%) | \- |
| Taxa de acerto: ajudou (%) | \- |
| Tempo médio | \- |
| Tentativas por atendimento | \- |
| Facilidade média (1 a 5\) | \- |
| Dúvidas sem solução | \- |
| Melhoria realizada após o teste | \- |

## 10\. Limitações e decisões técnicas

- A busca é baseada em regras e palavras-chave; não é um modelo de inteligência artificial generativa e pode não compreender sinônimos que não estejam cadastrados.  
- O assistente só responde com informações incluídas no JSON e não substitui atendimento público nem análise jurídica individual.  
- A disponibilidade, os documentos exigidos e os procedimentos podem variar e mudar; por isso a fonte oficial deve ser consultada.  
- O bloqueio de dados pessoais é uma proteção simples por padrão de texto, não um mecanismo completo de detecção de todos os dados sensíveis.

## 11\. vídeo

\-