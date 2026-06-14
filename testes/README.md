# Processo de Teste de Software — MotoAR 🧪

Esta pasta centraliza todas as atividades, especificações e resultados relacionados à aplicação do **Processo de Teste de Software** no projeto integrador **MotoAR**, conforme as diretrizes acadêmicas de Qualidade e Teste de Software (TQS).

---

## 📋 Conteúdo da Pasta de Testes

Esta pasta contém os seguintes artefatos:

1. **`test_motoar.py`**: Suíte de testes unitários automatizada desenvolvida com o framework **PyUnit** (`unittest`). Valida a corretude lógica de todas as regras de negócio em `motoar_logic.py`.
2. **`1_Plano_de_Testes.md`**: Plano de testes completo preenchido conforme o modelo original (`1-TQS-Modelo de Plano de Testes.docx`), definindo o escopo, prioridades, recursos e cronograma de teste.
3. **`2_Casos_de_Teste.md`**: Roteiro e especificação técnica detalhada de cada caso de teste de caixa preta e caixa branca, baseado no modelo original (`2-TQS-Modelo de Casos de Teste.docx`).
4. **`3_Registros_de_Testes.md`**: Relatório de execução e logs contendo as evidências reais de sucesso de todas as asserções rodadas no PyUnit.

---

## 🚀 Como Executar os Testes Automatizados (PyUnit)

Para rodar os testes de unidade de forma automática, abra o seu terminal na pasta raiz do projeto (`Atividade PI lll`) e digite o seguinte comando:

```bash
python -m unittest testes/test_motoar.py
```

O comando executará todas as classes de teste e imprimirá um relatório resumido.

### Para execução detalhada (modo verbose):

```bash
python -m unittest -v testes/test_motoar.py
```

---

## 🔍 Cobertura e Técnicas Aplicadas

O processo foi modelado sob duas perspectivas metodológicas principais:

### 1. Testes de Caixa Preta (Funcionais)
* **Particionamento de Equivalência (Classes de Equivalência)**: Aplicado para garantir que dados válidos (como meses de 1 a 12) retornem a classificação correta ("Chuva", "Seca", "Transição") e dados inválidos (como strings ou números fora do range) sejam tratados de forma segura retornando `"Desconhecido"`.
* **Análise do Valor Limite**: Utilizado para testar as fronteiras exatas da fórmula do MotoAR Score e da listagem de recomendações de equipamentos (Gear), validando os thresholds recomendados pela OMS para material particulado PM2.5 (12 µg/m³, 15 µg/m³ e 25 µg/m³).

### 2. Testes de Caixa Branca (Estruturais)
* **Cobertura de Desvio (Branch Coverage)**: Desenho de testes para executar todas as ramificações de código condicional (`if/elif/else`) das funções de risco e de gear em `motoar_logic.py`, garantindo que nenhuma linha de decisão lógica fique sem validação.
* **Tratamento de Exceções**: Testagem estrutural de comportamento da aplicação diante de dados inconsistentes de sensores (como valores nulos `None` ou `NaN` em temperaturas, umidades e ventos), assegurando que o sistema manipula os erros sem causar travamentos inesperados (crashes).
