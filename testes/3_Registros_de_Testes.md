# Registros de Testes — Projeto MotoAR

**Projeto:** MotoAR — Análise de Qualidade do Ar para Motociclistas  
**Versão:** 1.0  
**Equipe:** Giovani  
**Local e Data:** Brasília-DF, 14 de Junho de 2026  

---

## 💻 Ambiente de Execução dos Testes

* **Sistema Operacional:** Windows
* **Interpretador Python:** Python 3.13.0
* **Framework de Testes:** PyUnit (`unittest` v3.13)
* **Modo de Execução:** Linha de Comando (PowerShell)

---

## 📊 Resumo de Execução dos Testes

| Módulo de Teste | Casos de Teste Planejados | Executados | Sucesso | Falha | Erro | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `TestCleanHelpers` | 3 | 3 | 3 | 0 | 0 | 🟢 PASS |
| `TestMapSeason` | 2 | 2 | 2 | 0 | 0 | 🟢 PASS |
| `TestCalculateScore` | 6 | 6 | 6 | 0 | 0 | 🟢 PASS |
| `TestScoreClassification` | 1 | 1 | 1 | 0 | 0 | 🟢 PASS |
| `TestRecommendGear` | 4 | 4 | 4 | 0 | 0 | 🟢 PASS |
| `TestPrepareFeatures` | 1 | 1 | 1 | 0 | 0 | 🟢 PASS |
| **Total Geral** | **17** | **17** | **17** | **0** | **0** | **🟢 SUCESSO** |

---

## 📝 Log Completo de Execução (Console PyUnit)

O comando abaixo foi executado no terminal raiz do projeto:
```powershell
python -m unittest -v testes/test_motoar.py
```

```text
test_boundaries (testes.test_motoar.TestCalculateScore.test_boundaries) ... ok
test_clean_air_dry_season (testes.test_motoar.TestCalculateScore.test_clean_air_dry_season) ... ok
test_clean_air_wet_season (testes.test_motoar.TestCalculateScore.test_clean_air_wet_season) ... ok
test_heavy_pollution (testes.test_motoar.TestCalculateScore.test_heavy_pollution) ... ok
test_invalid_inputs (testes.test_motoar.TestCalculateScore.test_invalid_inputs) ... ok
test_moderate_pollution (testes.test_motoar.TestCalculateScore.test_moderate_pollution) ... ok
test_clean_humidity (testes.test_motoar.TestCleanHelpers.test_clean_humidity) ... ok
test_clean_temperature (testes.test_motoar.TestCleanHelpers.test_clean_temperature) ... ok
test_clean_wind_speed (testes.test_motoar.TestCleanHelpers.test_clean_wind_speed) ... ok
test_invalid_months (testes.test_motoar.TestMapSeason.test_invalid_months) ... ok
test_valid_seasons (testes.test_motoar.TestMapSeason.test_valid_seasons) ... ok
test_feature_engineering_math (testes.test_motoar.TestPrepareFeatures.test_feature_engineering_math) ... ok
test_cold_months (testes.test_motoar.TestRecommendGear.test_cold_months) ... ok
test_default_gear (testes.test_motoar.TestRecommendGear.test_default_gear) ... ok
test_no2_and_rain (testes.test_motoar.TestRecommendGear.test_no2_and_rain) ... ok
test_pm25_recommendations (testes.test_motoar.TestRecommendGear.test_pm25_recommendations) ... ok
test_classifications (testes.test_motoar.TestScoreClassification.test_classifications) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.075s

OK
```
