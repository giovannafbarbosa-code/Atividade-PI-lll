# MotoAR — Análise de Qualidade do Ar para Motociclistas 🏍️

Este projeto é um aplicativo analítico e preditivo desenvolvido em **Streamlit** voltado para auxiliar motociclistas de Brasília-DF a tomarem decisões de viagem seguras com base na qualidade do ar e condições meteorológicas.
O MotoAR consolida dados históricos e de quasi-tempo real das estações automáticas do **INMET** (CRAS Fercal) e de sensores da **IQAir** para simular e estimar a poluição por material particulado fino (**PM2.5**).

---

## 🏗️ Arquitetura do Projeto e Testabilidade

Para atender aos requisitos de qualidade e permitir a aplicação de um **Processo de Teste de Software (PyUnit)** estruturado, o código original foi refatorado seguindo o princípio da **Separação de Preocupações (Separation of Concerns)**:

1. **`motoar_logic.py` (Camada de Lógica)**: Módulo independente que contém apenas funções matemáticas puras, regras de negócio e de processamento de dados (ex: limpeza de strings, mapeamento sazonal, fórmula de score, regras de Gear e engenharia de features para o XGBoost). Esta camada não possui dependências com o Streamlit, tornando-se **100% testável** de forma automatizada.
2. **`motoar_app2.py` (Camada de Apresentação)**: Arquivo Streamlit responsável exclusivo pela interface com o usuário (UI), renderização de gráficos do Plotly, painel interativo (sliders) e exportação de PDF. Ele importa a lógica pura de `motoar_logic.py`.

---

## 📁 Estrutura de Pastas

```
C:\Users\giova\OneDrive\Documentos\Atividade PI lll\
├── README.md                          <-- Este arquivo (documentação principal)
├── motoar_app2.py                     <-- Interface gráfica e execução Streamlit
├── motoar_logic.py                    <-- Regras de negócio puras (Testável)
├── iqair_clean.csv                    <-- Base de dados de entrada da IQAir
├── ESTACOES AUTOMATICAS _ DADOS BRUTO 2025.xlsx <-- Base de dados de entrada do INMET
├── 1-TQS-Modelo de Plano de Testes.docx <-- Modelo original do Plano de Testes
├── 2-TQS-Modelo de Casos de Teste.docx  <-- Modelo original dos Casos de Teste
└── testes/                            <-- Diretório contendo os artefatos de teste
    ├── README.md                      <-- Documentação de execução e resultados dos testes
    ├── test_motoar.py                 <-- Suíte de testes automatizados (PyUnit)
    ├── 1_Plano_de_Testes.md           <-- Plano de Testes preenchido
    ├── 2_Casos_de_Teste.md            <-- Especificação de Casos de Teste preenchidos
    └── 3_Registros_de_Testes.md       <-- Logs e registros da execução dos testes
```

---

## 🛠️ Como Instalar as Dependências

Antes de rodar a aplicação ou executar os testes, certifique-se de possuir o Python instalado (recomendado >= 3.9) e instale as bibliotecas necessárias rodando o seguinte comando no seu terminal:

```bash
pip install streamlit plotly pandas scikit-learn xgboost openpyxl reportlab
```

---

## 🚀 Como Executar o Aplicativo

Para inicializar a interface visual do MotoAR no seu navegador local, execute o seguinte comando no terminal (dentro da pasta raiz do projeto):

```bash
streamlit run motoar_app2.py
```

O Streamlit abrirá uma aba automaticamente no seu navegador no endereço: `http://localhost:8501`.

---

## 🧪 Processo de Testes

Os arquivos de testes automatizados, plano de testes, especificação de casos e logs estão organizados de forma dedicada dentro do diretório `testes/`.
Para mais informações sobre como executar e verificar os testes unitários do PyUnit, consulte o arquivo [testes/README.md](testes/README.md).
