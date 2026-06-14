import unittest
import numpy as np
import pandas as pd
import sys
import os

# Adiciona o diretório pai ao path para importar o motoar_logic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import motoar_logic as ml

class TestCleanHelpers(unittest.TestCase):
    def test_clean_temperature(self):
        self.assertEqual(ml.clean_temperature("25°C"), 25.0)
        self.assertEqual(ml.clean_temperature("  -3.5 °C  "), -3.5)
        self.assertEqual(ml.clean_temperature("30"), 30.0)
        self.assertTrue(np.isnan(ml.clean_temperature(np.nan)))
        self.assertTrue(np.isnan(ml.clean_temperature(None)))
        self.assertTrue(np.isnan(ml.clean_temperature("invalid")))

    def test_clean_humidity(self):
        self.assertEqual(ml.clean_humidity("80%"), 80.0)
        self.assertEqual(ml.clean_humidity("  95.5 %  "), 95.5)
        self.assertEqual(ml.clean_humidity("50"), 50.0)
        self.assertTrue(np.isnan(ml.clean_humidity(np.nan)))
        self.assertTrue(np.isnan(ml.clean_humidity(None)))
        self.assertTrue(np.isnan(ml.clean_humidity("invalid")))

    def test_clean_wind_speed(self):
        self.assertEqual(ml.clean_wind_speed("15km/h"), 15.0)
        self.assertEqual(ml.clean_wind_speed("  20.3 km/h  "), 20.3)
        self.assertEqual(ml.clean_wind_speed("10"), 10.0)
        self.assertTrue(np.isnan(ml.clean_wind_speed(np.nan)))
        self.assertTrue(np.isnan(ml.clean_wind_speed(None)))
        self.assertTrue(np.isnan(ml.clean_wind_speed("invalid")))

class TestMapSeason(unittest.TestCase):
    def test_valid_seasons(self):
        # Meses de Chuva: 1 a 6
        for m in range(1, 7):
            self.assertEqual(ml.map_season(m), "🌧️ Chuva")
        
        # Meses de Seca: 7 a 10
        for m in range(7, 11):
            self.assertEqual(ml.map_season(m), "🔥 Seca")
            
        # Meses de Transição: 11 e 12
        for m in [11, 12]:
            self.assertEqual(ml.map_season(m), "🍂 Transição")

    def test_invalid_months(self):
        self.assertEqual(ml.map_season(0), "Desconhecido")
        self.assertEqual(ml.map_season(13), "Desconhecido")
        self.assertEqual(ml.map_season("abc"), "Desconhecido")
        self.assertEqual(ml.map_season(None), "Desconhecido")

class TestCalculateScore(unittest.TestCase):
    def test_clean_air_wet_season(self):
        # PM2.5 = 0, Sem seca -> score 100
        self.assertEqual(ml.calculate_score(0, False), 100)

    def test_clean_air_dry_season(self):
        # PM2.5 = 0, Com seca -> score 90 (penalidade de 10)
        self.assertEqual(ml.calculate_score(0, True), 90)

    def test_moderate_pollution(self):
        # PM2.5 = 25 (metade de 50), Sem seca -> score = 100 - (25/50)*80 = 60
        self.assertEqual(ml.calculate_score(25, False), 60)

    def test_heavy_pollution(self):
        # PM2.5 = 100, Sem seca -> score = max(0, 100 - (100/50)*80) = 0
        self.assertEqual(ml.calculate_score(100, False), 0)

    def test_boundaries(self):
        # Testar valor negativo de PM2.5 (deve limitar em 100)
        self.assertEqual(ml.calculate_score(-10, False), 100)
        # Testar valor extremamente alto (deve limitar em 0)
        self.assertEqual(ml.calculate_score(500, True), 0)

    def test_invalid_inputs(self):
        # Testar com strings ou None
        self.assertEqual(ml.calculate_score("abc", False), 100)
        self.assertEqual(ml.calculate_score(None, False), 100)

class TestScoreClassification(unittest.TestCase):
    def test_classifications(self):
        # Ótimo: >= 75
        lbl, color = ml.get_score_classification(75)
        self.assertEqual(lbl, "Ótimo para sair")
        self.assertEqual(color, "green")

        # Bom: 65 a 74
        lbl, color = ml.get_score_classification(70)
        self.assertEqual(lbl, "Bom para sair")
        self.assertEqual(color, "blue")

        # Favorável: 55 a 64
        lbl, color = ml.get_score_classification(60)
        self.assertEqual(lbl, "Favorável")
        self.assertEqual(color, "yellow")

        # Máscara N95: 45 a 54
        lbl, color = ml.get_score_classification(50)
        self.assertEqual(lbl, "Use máscara N95")
        self.assertEqual(color, "orange")

        # Filtro de ar: 35 a 44
        lbl, color = ml.get_score_classification(40)
        self.assertEqual(lbl, "Use filtro de ar")
        self.assertEqual(color, "orange")

        # Evitar: < 35
        lbl, color = ml.get_score_classification(30)
        self.assertEqual(lbl, "Evite ou use EPI completo")
        self.assertEqual(color, "red")

class TestRecommendGear(unittest.TestCase):
    def test_default_gear(self):
        # Condições excelentes
        gear = ml.recommend_gear(pm25_pred=5, no2=10, rain=0, month=1)
        self.assertIn("✅ Condições favoráveis — equipamento padrão suficiente", gear)
        self.assertEqual(len(gear), 1)

    def test_pm25_recommendations(self):
        # PM2.5 > 12: Capacete com filtro
        gear = ml.recommend_gear(pm25_pred=13, no2=10, rain=0, month=1)
        self.assertIn("🪖 Capacete com filtro de ar — PM2.5 elevado", gear)
        self.assertNotIn("⚠️ Atenção extra — PM2.5 acima do recomendado pela OMS", gear)

        # PM2.5 > 15: Atenção extra OMS
        gear = ml.recommend_gear(pm25_pred=18, no2=10, rain=0, month=1)
        self.assertIn("🪖 Capacete com filtro de ar — PM2.5 elevado", gear)
        self.assertIn("⚠️ Atenção extra — PM2.5 acima do recomendado pela OMS", gear)
        self.assertNotIn("😷 Máscara N95 recomendada — nível preocupante", gear)

        # PM2.5 > 25: Máscara N95
        gear = ml.recommend_gear(pm25_pred=28, no2=10, rain=0, month=1)
        self.assertIn("🪖 Capacete com filtro de ar — PM2.5 elevado", gear)
        self.assertIn("⚠️ Atenção extra — PM2.5 acima do recomendado pela OMS", gear)
        self.assertIn("😷 Máscara N95 recomendada — nível preocupante", gear)

    def test_no2_and_rain(self):
        # NO2 > 40 e Rain > 5
        gear = ml.recommend_gear(pm25_pred=5, no2=45, rain=6, month=1)
        self.assertIn("🕶️ Viseira fechada — NO2 elevado", gear)
        self.assertIn("🌂 Capa de chuva — precipitação recente", gear)
        self.assertNotIn("✅ Condições favoráveis — equipamento padrão suficiente", gear)

    def test_cold_months(self):
        # Meses frios (6, 7, 8)
        gear = ml.recommend_gear(pm25_pred=5, no2=10, rain=0, month=7)
        self.assertIn("🧥 Jaqueta com forro — mês mais frio", gear)

class TestPrepareFeatures(unittest.TestCase):
    def test_feature_engineering_math(self):
        # Criar dataframe dummy
        data = {
            "hour": [0, 6, 12, 18],
            "month": [1, 4, 7, 10],
            "pm25": [10.0, 15.0, 20.0, 25.0],
            "rain": [0.0, 1.0, 0.0, 10.0]
        }
        df = pd.DataFrame(data)
        processed = ml.prepare_features(df)

        # Verificar se as novas colunas foram geradas
        expected_cols = [
            "hour_sin", "hour_cos", "month_sin", "month_cos", 
            "is_dry", "pm25_lag1", "pm25_lag3", "pm25_roll3", "rain_acc6"
        ]
        for col in expected_cols:
            self.assertIn(col, processed.columns)

        # Testar flag is_dry (meses 7 e 10 devem ser 1, 1 e 4 devem ser 0)
        self.assertEqual(processed.loc[0, "is_dry"], 0)
        self.assertEqual(processed.loc[1, "is_dry"], 0)
        self.assertEqual(processed.loc[2, "is_dry"], 1)
        self.assertEqual(processed.loc[3, "is_dry"], 1)

        # Testar a transformação de seno da hora (hora 0 e 12)
        # np.sin(0) = 0, np.sin(2 * pi * 12 / 24) = np.sin(pi) = 0
        self.assertAlmostEqual(processed.loc[0, "hour_sin"], 0.0)
        self.assertAlmostEqual(processed.loc[2, "hour_sin"], 0.0)

if __name__ == '__main__':
    unittest.main()
