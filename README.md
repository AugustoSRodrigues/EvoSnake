# 🐍 EvoSnake: Um Agente Evolutivo para o Jogo da Cobrinha

Este projeto implementa um agente autônomo para o clássico jogo da cobrinha (Snake), treinado com base no paradigma de **Sistemas Classificadores** — uma abordagem inspirada em sistemas adaptativos complexos e algoritmos genéticos.

---

## 🧠 O que são Sistemas Classificadores?

Sistemas Classificadores são métodos de aprendizado que combinam regras de decisão com algoritmos evolutivos. Cada "classificador" é uma regra do tipo:

```
SE [condição] ENTÃO [ação]
```

Essas regras interagem com o ambiente, competem entre si, são recompensadas ou punidas com base em seu desempenho, e evoluem ao longo do tempo.

Neste projeto, usamos a **abordagem Michigan**, em que cada classificador representa uma regra individual, e a população inteira representa a solução.

---

## 🎮 Como o Agente Funciona?

O agente é uma população de regras que joga o jogo da cobrinha sem nenhuma intervenção humana. O processo ocorre em ciclos:

1. **Percepção do Ambiente**: 
   O agente gera uma mensagem binária representando o estado atual (direção da cabeça, obstáculos ao redor, direção da fruta).

2. **Seleção de Classificadores**:
   Regras cuja condição (antecedente) é compatível com a mensagem são selecionadas.

3. **Competição**:
   Os classificadores compatíveis "apostam" usando sua energia (`strength`). O vencedor (com maior *lance efetivo*, ou `ebid`) escolhe a ação da cobrinha.

4. **Execução e Feedback**:
   A ação é realizada no ambiente. O classificador vencedor é então recompensado (se a ação for positiva, como pegar a fruta) ou punido (por bater ou se afastar da fruta).

5. **Evolução**:
   Após um número de iterações, os melhores classificadores se reproduzem via *crossover* e *mutação*, gerando novos filhos que substituem os piores.

---

## 📁 Estrutura do Projeto

- `snake.py`: Script principal que contém todo o código do agente, lógica evolutiva e ambiente do jogo.
- `topico_11_sistemas_classificadores.pdf`: Referência teórica usada como base conceitual do projeto.

---

## ⚙️ Principais Componentes do Código

- **Geração da Mensagem (`geracao_msg`)**: Codifica o ambiente em bits: direção da cobra, presença de obstáculos, posição da fruta, etc.
- **Regras (Classificadores)**: São vetores com parte antecedente (condição) e consequente (ação).
- **Funções de Evolução**:
  - `taxa(n)`: Define taxa de vida de um classificador.
  - `bit` / `ebit`: Calculam os lances e o ruído da competição.
  - `reproducao` e `mutacao`: Realizam os operadores genéticos.
- **Avaliação (`recompensa`)**: Define como a energia de um classificador muda após uma ação.

---

## 📊 Métricas Coletadas

O código mede:
- Quantas vezes a cobra morreu por bater no corpo ou nas paredes.
- Quantos movimentos foram necessários para alcançar a fruta.
- Pontuação média por geração.

Esses dados ajudam a visualizar a **melhoria evolutiva do comportamento do agente** ao longo das iterações.

---

## ▶️ Como Rodar

Requisitos:
- Python 3.8+
- `pygame`, `numpy`

Instale os pacotes:

```bash
pip install pygame numpy
```

Execute o script:

```bash
python snake.py
```

Durante a execução, pressione **barra de espaço** para encerrar o jogo manualmente.

---



## 📚 Referência

Este trabalho se baseia no conteúdo didático do **Tópico 11 – Sistemas Classificadores** do Prof. Von Zuben et al. (UNICAMP), utilizando conceitos como:
- Codificação ternária com símbolo `#` (don't care)
- Apropriação de crédito
- Competição via lances e ruído gaussiano
- Evolução genética via seleção, crossover e mutação
