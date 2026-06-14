# Plano de Testes — Projeto MotoAR

**Projeto:** MotoAR — Análise de Qualidade do Ar para Motociclistas  
**Versão:** 1.0  
**Equipe:** Giovani  
**Local e Data:** Brasília-DF, 14 de Junho de 2026  

---

## Histórico de Revisões

| Data | Versão | Descrição | Autor(es) |
| :--- | :--- | :--- | :--- |
| 14/06/2026 | 1.0 | Versão inicial do Plano de Testes do MotoAR | Giovani |

---

## Sumário
1. [Introdução](#1-introdução)
2. [Objetivos e Escopo dos Testes](#2-objetivos-e-escopo-dos-testes)
3. [Estratégia de Testes](#3-estratégia-de-testes)
4. [Níveis de Teste](#4-níveis-de-teste)
5. [Tipos e Cobertura dos Testes](#5-tipos-e-cobertura-dos-testes)
6. [Técnicas de Teste](#6-técnicas-de-teste)
7. [Cronograma de Testes e Recursos Necessários](#7-cronograma-de-testes-e-recursos-necessários)
8. [Ferramentas de Teste](#8-ferramentas-de-teste)
9. [Gerenciamento dos Testes](#9-gerenciamento-dos-testes)

---

## 1. Introdução

Este documento descreve o plano de testes para o projeto **MotoAR**.
O MotoAR é uma aplicação analítica e preditiva (desenvolvida em Streamlit) voltada para motociclistas de Brasília. O sistema combina dados meteorológicos e de poluentes provenientes de estações automáticas do INMET (CRAS Fercal) e sensores de quasi-tempo real da IQAir para:
1. Calcular e exibir a sazonalidade e padrões diários dos poluentes (especialmente material particulado PM2.5).
2. Treinar um modelo preditivo baseado em Machine Learning (XGBoost/Gradient Boosting) para estimar os níveis de PM2.5 futuros.
3. Gerar um **MotoAR Score** (0 a 100) que indica as condições para conduzir motocicleta.
4. Recomendar equipamentos de segurança apropriados (Gear) e gerar relatórios executivos em formato PDF.

---

## 2. Objetivos e Escopo dos Testes

### Objetivos:
- Garantir que a limpeza dos dados textuais de entrada de sensores (como remoção de unidades "°C", "%" e "km/h") seja realizada com exatidão.
- Assegurar a corretude matemática do cálculo do MotoAR Score e suas classificações qualitativas ("Ótimo para sair", "Evite", etc.).
- Validar as regras de recomendação de equipamentos sob diferentes thresholds climáticos e de qualidade do ar.
- Assegurar que o algoritmo de preparação de features (Feature Engineering) gera adequadamente lags e transformações de seno/cosseno para o modelo preditivo.
- Garantir que o aplicativo permaneça funcional e íntegro após a refatoração estrutural (separação da lógica de negócios e UI).

### Inclusões (No Escopo):
- Lógica de limpeza de dados (temperatura, umidade, velocidade do vento).
- Mapeamento de sazonalidade (estação seca, chuvosa e transição baseada nos meses).
- Cálculo do MotoAR Score e seus limites de valor (boundaries).
- Algoritmo de decisão das recomendações de equipamentos de proteção (Gear).
- Processamento matemático de variáveis temporais (hour_sin, month_sin, etc.) para o modelo preditivo.
- Integração da interface visual Streamlit com as regras de negócio refatoradas.

### Exclusões (Fora do Escopo):
- Testes de precisão estatística do modelo preditivo XGBoost em tempo real (o teste valida apenas o fluxo de engenharia de features e chamada, não a acurácia de convergência do modelo).
- Validação física da API externa do IQAir ou Open-Meteo (serão utilizados dados locais em formato CSV/XLSX).
- Testes de estresse de tráfego de rede concorrente e segurança de infraestrutura do servidor Streamlit.

---

## 3. Estratégia de Testes

### Abordagem:
Adotaremos uma abordagem de testes híbrida:
1. **Testes Unitários Automatizados (Caixa Branca)**: Implementados via biblioteca `unittest` (PyUnit) do Python, focados nas funções puras de lógica contidas em `motoar_logic.py`.
2. **Testes Funcionais Manuais (Caixa Preta)**: Validação de fluxo ponta a ponta na interface visual do Streamlit, simulando entradas do usuário através de sliders e selects, garantindo a atualização correta do dashboard e do relatório PDF.

### Riscos e Mitigações:
- **Risco:** Erros de importação e quebra da aplicação Streamlit após a refatoração.
  - *Mitigação:* Execução imediata da suíte de testes unitários PyUnit e posterior execução do servidor de homologação Streamlit para checagem visual de regressão.
- **Risco:** Ausência dos arquivos brutos de dados para o carregamento do cache no ambiente de teste.
  - *Mitigação:* Implementação de fallbacks inteligentes de arquivos no código (`iqair_clean.csv` e `ESTACOES AUTOMATICAS _ DADOS BRUTO 2025.xlsx`) para carregar automaticamente arquivos reais presentes no diretório raiz.

### Priorização:
Os testes serão priorizados conforme a criticidade:
- **Prioridade Alta:** Funções de cálculo do Score e higienização dos dados do sensor (bloqueantes para o uso seguro do motociclista).
- **Prioridade Média:** Regras de Gear e geração de features temporais.
- **Prioridade Baixa:** Formatação visual das cores do Score e exportação para PDF.

---

## 4. Níveis de Teste

- **Testes Unitários**: Aplicados no nível de componente, testando individualmente cada função de `motoar_logic.py` com valores extremos, nulos e inválidos de entrada.
- **Testes de Integração**: Validação da interação entre a preparação de features em `motoar_logic.py` e o pipeline de modelagem preditiva em `motoar_app2.py` (XGBoost).
- **Testes de Sistema**: Validação de ponta a ponta do aplicativo executado via Streamlit, verificando se o carregamento de planilhas locais e a simulação de sliders geram os elementos corretos na tela.
- **Testes de Aceitação (Homologação)**: Apresentação da ferramenta final ao usuário, coletando feedback sobre a interface gráfica e usabilidade das recomendações geradas para Brasília.

---

## 5. Tipos e Cobertura dos Testes

- **Testes de Caixa Branca (Estruturais)**: Aplicados sobre a estrutura lógica de decisão de `motoar_logic.py`. Garantiremos a cobertura de 100% das decisões condicionais (branches) para o cálculo do Score e classificação, bem como o tratamento correto de exceções (`TypeError`, `ValueError`).
- **Testes de Caixa Preta (Funcionais)**: Focados em validar se as saídas para as interfaces estão de acordo com as regras de trânsito climáticas estabelecidas para o motociclista.

---

## 6. Técnicas de Teste

### Técnicas de Caixa Preta:
- **Particionamento de Equivalência (Classes de Equivalência)**: Divisão de valores válidos e inválidos. Exemplo: Para meses, o intervalo válido é [1, 12]. Valores <= 0, >= 13 ou strings devem retornar "Desconhecido".
- **Análise do Valor Limite (Boundary Value Analysis)**: Focado nas bordas de decisão do score. Exemplo: Limiar de qualidade do ar da OMS (12 µg/m³, 15 µg/m³, 25 µg/m³), testando o comportamento com valores exatamente iguais, imediatamente abaixo e imediatamente acima.

### Técnicas de Caixa Branca:
- **Cobertura de Desvio (Branch Coverage)**: Garante que todos os caminhos dos blocos `if/elif/else` em `get_score_classification` e `recommend_gear` sejam testados (ex: cobrindo cada um dos 6 estados de classificação de score).

---

## 7. Cronograma de Testes e Recursos Necessários

### Cronograma:

| Etapa / Fase dos Testes | Data Início | Data Fim | Responsável |
| :--- | :--- | :--- | :--- |
| Planejamento e Elaboração do Plano | 14/06/2026 | 14/06/2026 | Giovani |
| Refatoração e Configuração do Ambiente | 14/06/2026 | 14/06/2026 | Giovani |
| Codificação dos Testes Unitários | 14/06/2026 | 14/06/2026 | Giovani |
| Execução dos Testes Automatizados (PyUnit) | 14/06/2026 | 14/06/2026 | Giovani |
| Teste de Regressão e Validação do Streamlit | 14/06/2026 | 15/06/2026 | Giovani |
| Homologação e Entrega dos Artefatos | 15/06/2026 | 19/06/2026 | Giovani |

### Recursos Necessários:
- **Recursos Humanos:** 1 Analista de Testes / Desenvolvedor (Giovani).
- **Ambiente de Testes:** Máquina local com Windows, Python 3.13 e os datasets do INMET e IQAir.
- **Ferramentas:** VS Code, Git e Terminal PowerShell.

---

## 8. Ferramentas de Teste

- **PyUnit (unittest)**: Framework nativo de testes do Python utilizado para a automação e verificação dos métodos lógicos.
- **Pandas & NumPy**: Utilizados para mockar pequenos DataFrames nos testes da engenharia de features.
- **Pip**: Gerenciador de pacotes para a instalação de bibliotecas como `streamlit`, `scikit-learn` e `xgboost`.

---

## 9. Gerenciamento dos Testes

- **Critérios de Aceitação de Testes**: Um caso de teste automatizado é considerado bem-sucedido se sua asserção (`self.assertEqual`, etc.) retornar verdadeira e o teste não gerar erros/exceções.
- **Registro de Defeitos**: Defeitos serão corrigidos imediatamente pelo desenvolvedor na mesma iteração de desenvolvimento.
- **Evidências de Teste**: Os resultados da execução do PyUnit serão direcionados para o arquivo `3_Registros_de_Testes.md`.
- **Aprovação**: O plano e registros serão submetidos para aprovação final no contexto do Projeto Integrador até o dia 19/06.
