# Casos de Teste — Projeto MotoAR

**Projeto:** MotoAR — Análise de Qualidade do Ar para Motociclistas  
**Versão:** 1.0  
**Equipe:** Giovani  
**Local e Data:** Brasília-DF, 14 de Junho de 2026  

---

## Histórico de Revisões

| Data | Versão | Descrição | Autor(es) |
| :--- | :--- | :--- | :--- |
| 14/06/2026 | 1.0 | Elaboração dos casos de teste unitários e de sistema | Giovani |

---

## Casos de Teste Detalhados

### CT 001 - Higienização da Temperatura
* **Caso de Teste #:** CT 001 - Higienização da Temperatura
* **Prioridade:** Média
* **Caso de Uso / Requisito:** RF 001 - Ingestão e Limpeza de Dados do Sensor
* **Objetivo do Teste:** Verificar se a string de temperatura contendo caracteres de unidade ("°C") e espaços extras é limpa e convertida corretamente para o formato numérico float.
* **Localização:** `motoar_logic.py` > `clean_temperature`
* **Pré-Condições:** Módulo `motoar_logic` carregado.
* **Dados de Entrada:**
  - Entrada A: `"25°C"` (limpeza padrão)
  - Entrada B: `"  -3.5 °C  "` (valores negativos e espaços extras)
  - Entrada C: `None` ou `np.nan` (valores nulos)
* **Procedimento:**
  1. Invocar a função `clean_temperature` passando a Entrada A e armazenar o resultado.
  2. Invocar a função `clean_temperature` passando a Entrada B e armazenar o resultado.
  3. Invocar a função `clean_temperature` passando a Entrada C e armazenar o resultado.
* **Resultado Esperado:**
  - O resultado da Entrada A deve ser exatamente o float `25.0`.
  - O resultado da Entrada B deve ser exatamente o float `-3.5`.
  - O resultado da Entrada C deve ser `np.nan`.
* **Pós-Condições:** Os valores limpos estão prontos para operações matemáticas e estatísticas.
* **Notas Adicionais:** Testado de forma automatizada via `test_motoar.py`.

---

### CT 002 - Mapeamento Sazonal (Meses do Ano)
* **Caso de Teste #:** CT 002 - Mapeamento Sazonal (Meses do Ano)
* **Prioridade:** Média
* **Caso de Uso / Requisito:** RF 002 - Classificação Sazonal dos Dados
* **Objetivo do Teste:** Validar se os meses do ano são mapeados para a respectiva estação de Brasília (Chuva, Seca ou Transição).
* **Localização:** `motoar_logic.py` > `map_season`
* **Pré-Condições:** Módulo `motoar_logic` carregado.
* **Dados de Entrada:**
  - Entrada A: Mês `1` (Janeiro)
  - Entrada B: Mês `8` (Agosto)
  - Entrada C: Mês `11` (Novembro)
  - Entrada D: Mês `13` ou `"abc"` (inválidos)
* **Procedimento:**
  1. Chamar `map_season(1)`
  2. Chamar `map_season(8)`
  3. Chamar `map_season(11)`
  4. Chamar `map_season(13)` e `map_season("abc")`
* **Resultado Esperado:**
  - Retorno da Entrada A deve ser `"🌧️ Chuva"`
  - Retorno da Entrada B deve ser `"🔥 Seca"`
  - Retorno da Entrada C deve ser `"🍂 Transição"`
  - Retorno da Entrada D deve ser `"Desconhecido"`
* **Pós-Condições:** O dado classificado da estação é adicionado à série histórica para agregação gráfica.
* **Notas Adicionais:** Crucial para o cálculo da sazonalidade gráfica e do score.

---

### CT 003 - Cálculo do MotoAR Score com Penalidade Sazonal
* **Caso de Teste #:** CT 003 - Cálculo do MotoAR Score
* **Prioridade:** Alta
* **Caso de Uso / Requisito:** RF 003 - Algoritmo do MotoAR Score para Saída
* **Objetivo do Teste:** Verificar se a fórmula matemática do score de saída (0-100) responde corretamente aos níveis de PM2.5 e aplica a penalidade de 10 pontos durante a estação seca (is_dry = True).
* **Localização:** `motoar_logic.py` > `calculate_score`
* **Pré-Condições:** Fórmulas de cálculo implementadas.
* **Dados de Entrada:**
  - Cenário A: `pm25_pred = 0`, `is_dry = False` (Ar puro, época de chuva)
  - Cenário B: `pm25_pred = 0`, `is_dry = True` (Ar puro, época de seca)
  - Cenário C: `pm25_pred = 25`, `is_dry = False` (Poluição moderada)
  - Cenário D: `pm25_pred = 100`, `is_dry = False` (Poluição severa)
* **Procedimento:**
  1. Executar `calculate_score(0, False)`
  2. Executar `calculate_score(0, True)`
  3. Executar `calculate_score(25, False)`
  4. Executar `calculate_score(100, False)`
* **Resultado Esperado:**
  - Cenário A: Score deve ser exatamente `100`
  - Cenário B: Score deve ser exatamente `90` (penalidade aplicada)
  - Cenário C: Score deve ser exatamente `60` (100 - (25/50)*80 = 60)
  - Cenário D: Score deve ser exatamente `0` (limitado ao mínimo)
* **Pós-Condições:** O score de saída numérico é gerado no simulador e na tela principal.
* **Notas Adicionais:** O score é calculado a partir de: `100 - (pm25_pred / 50) * 80 - (is_dry * 10)`.

---

### CT 004 - Classificação Qualitativa do Score (Limites de Risco)
* **Caso de Teste #:** CT 004 - Classificação Qualitativa do Score
* **Prioridade:** Alta
* **Caso de Uso / Requisito:** RF 004 - Classificação de Risco
* **Objetivo do Teste:** Validar que as faixas de score numéricas são traduzidas para as etiquetas textuais e chaves de cores CSS correspondentes.
* **Localização:** `motoar_logic.py` > `get_score_classification`
* **Pré-Condições:** MotoAR Score numérico válido.
* **Dados de Entrada:**
  - Entrada A: `score = 75` (Limite Ótimo)
  - Entrada B: `score = 65` (Limite Bom)
  - Entrada C: `score = 55` (Favorável)
  - Entrada D: `score = 45` (Use máscara)
  - Entrada E: `score = 35` (Use filtro de ar)
  - Entrada F: `score = 30` (Crítico)
* **Procedimento:**
  1. Chamar `get_score_classification` para cada um dos valores de entrada acima.
* **Resultado Esperado:**
  - Entrada A: `("Ótimo para sair", "green")`
  - Entrada B: `("Bom para sair", "blue")`
  - Entrada C: `("Favorável", "yellow")`
  - Entrada D: `("Use máscara N95", "orange")`
  - Entrada E: `("Use filtro de ar", "orange")`
  - Entrada F: `("Evite ou use EPI completo", "red")`
* **Pós-Condições:** A interface renderiza o badge visual com as cores corretas do tema.
* **Notas Adicionais:** Mapeamento visual testado de forma automatizada no PyUnit.

---

### CT 005 - Regra de Recomendação de Equipamento (Gear) sob Alta Poluição
* **Caso de Teste #:** CT 005 - Regra de Recomendação de Equipamento (Gear)
* **Prioridade:** Alta
* **Caso de Uso / Requisito:** RF 005 - Recomendador de Equipamento de Proteção
* **Objetivo do Teste:** Verificar se o sistema aciona as recomendações de equipamentos adequadas de acordo com thresholds climáticos de PM2.5, NO2, chuva e estação fria.
* **Localização:** `motoar_logic.py` > `recommend_gear`
* **Pré-Condições:** Funções de regras parametrizadas.
* **Dados de Entrada:**
  - Cenário A: `pm25_pred = 5`, `no2 = 10`, `rain = 0`, `month = 1` (Padrão)
  - Cenário B: `pm25_pred = 28`, `no2 = 45`, `rain = 6`, `month = 7` (Condição crítica)
* **Procedimento:**
  1. Executar `recommend_gear(5, 10, 0, 1)`
  2. Executar `recommend_gear(28, 45, 6, 7)`
* **Resultado Esperado:**
  - Cenário A: Retorna apenas a lista `["✅ Condições favoráveis — equipamento padrão suficiente"]`
  - Cenário B: Deve retornar uma lista contendo:
    - `"🪖 Capacete com filtro de ar — PM2.5 elevado"`
    - `"⚠️ Atenção extra — PM2.5 acima do recomendado pela OMS"`
    - `"😷 Máscara N95 recomendada — nível preocupante"`
    - `"🕶️ Viseira fechada — NO2 elevado"`
    - `"🌂 Capa de chuva — precipitação recente"`
    - `"🧥 Jaqueta com forro — mês mais frio"`
* **Pós-Condições:** A lista contendo todos os EPIs sugeridos é exibida em bullets na UI.
* **Notas Adicionais:** A lógica garante a segurança física do motociclista exposto a poluentes tóxicos (NO2) e particulados agressivos.

---

### CT 006 - Engenharia de Features para Machine Learning
* **Caso de Teste #:** CT 006 - Engenharia de Features para Machine Learning
* **Prioridade:** Média
* **Caso de Uso / Requisito:** RF 006 - Pipeline de Pré-processamento Preditivo
* **Objetivo do Teste:** Assegurar que o algoritmo de engenharia de features calcula corretamente as colunas seno/cosseno e lags/médias móveis de PM2.5.
* **Localização:** `motoar_logic.py` > `prepare_features`
* **Pré-Condições:** DataFrame bruto com colunas `hour`, `month`, `pm25` e `rain`.
* **Dados de Entrada:**
  - DataFrame dummy contendo 4 registros com variações de hora e mês.
* **Procedimento:**
  1. Passar o DataFrame de entrada para `prepare_features`
  2. Validar a presença das colunas geradas.
  3. Checar a flag `is_dry` baseada nos meses 7 e 10 (seca) vs 1 e 4 (chuva).
* **Resultado Esperado:**
  - As colunas `hour_sin`, `hour_cos`, `month_sin`, `month_cos`, `is_dry`, `pm25_lag1`, `pm25_lag3`, `pm25_roll3`, `rain_acc6` devem estar presentes.
  - A flag `is_dry` do registro no mês 7 deve ser `1`.
  - A flag `is_dry` do registro no mês 1 deve ser `0`.
* **Pós-Condições:** DataFrame preenchido é enviado com sucesso ao regressor XGBoost para treino ou predição.
* **Notas Adicionais:** Caso o DataFrame venha com valores nulos nas colunas bases, o processamento deve preencher com a média ou valor padrão sem gerar erro crítico.

---

### CT 007 - Simulação de Score em Tempo Real (Interface Streamlit)
* **Caso de Teste #:** CT 007 - Simulação de Score na Interface
* **Prioridade:** Alta
* **Caso de Uso / Requisito:** RF 007 - Simulador Interativo do Dashboard
* **Objetivo do Teste:** Validar se a interface gráfica responde à interação do usuário, recalculando o score e o gear exibidos na tela ao alterar os controles de entrada (Sliders).
* **Localização:** `motoar_app2.py` > Seção Simulador (Página "Modelo Preditivo")
* **Pré-Condições:** Servidor do Streamlit rodando localmente.
* **Dados de Entrada:** Interações na UI:
  - Mudar Slider "PM2.5 última hora" para `40.0 µg/m³`
  - Mudar Slider "Chuva acumulada 6h" para `10.0 mm`
* **Procedimento:**
  1. Abrir o navegador no endereço local do app (ex: `http://localhost:8501`).
  2. Ir até o menu de Navegação na barra lateral e selecionar a página "🤖 Modelo Preditivo".
  3. Rolar a página até a seção "Simulador — Índice de Saída do Motociclista".
  4. Arrastar o slider "PM2.5 última hora" para `40.0` e o slider "Chuva" para `10.0`.
  5. Observar o valor e cor do MotoAR Score e as recomendações de Gear atualizadas.
* **Resultado Esperado:**
  - O score exibido na tela deve recalcular dinamicamente de forma decrescente.
  - A máscara N95 e a capa de chuva devem aparecer instantaneamente no painel de "Gear recomendado".
* **Pós-Condições:** Os valores na tela refletem em tempo real as interações do motociclista.
* **Notas Adicionais:** Teste de caixa preta executado manualmente na homologação.
