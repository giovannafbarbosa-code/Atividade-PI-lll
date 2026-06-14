import pandas as pd
import numpy as np

def clean_temperature(val):
    """
    Cleans temperature string and converts to numeric.
    E.g. "25°C" -> 25.0
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).replace("°C", "").strip()
    return pd.to_numeric(val_str, errors="coerce")

def clean_humidity(val):
    """
    Cleans humidity string and converts to numeric.
    E.g. "80%" -> 80.0
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).replace("%", "").strip()
    return pd.to_numeric(val_str, errors="coerce")

def clean_wind_speed(val):
    """
    Cleans wind speed string and converts to numeric.
    E.g. "15km/h" -> 15.0
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).replace("km/h", "").strip()
    return pd.to_numeric(val_str, errors="coerce")

def map_season(month):
    """
    Maps month to season category.
    """
    seasons = {
        1: "🌧️ Chuva", 2: "🌧️ Chuva", 3: "🌧️ Chuva",
        4: "🌧️ Chuva", 5: "🌧️ Chuva", 6: "🌧️ Chuva",
        7: "🔥 Seca",  8: "🔥 Seca",  9: "🔥 Seca", 10: "🔥 Seca",
        11: "🍂 Transição", 12: "🍂 Transição"
    }
    try:
        m = int(month)
        return seasons.get(m, "Desconhecido")
    except (ValueError, TypeError):
        return "Desconhecido"

def calculate_score(pm25_pred, is_dry):
    """
    Calculates MotoAR Score (0 to 100).
    A lower PM2.5 results in a higher score.
    """
    try:
        pm25 = float(pm25_pred)
    except (ValueError, TypeError):
        pm25 = 0.0
    dry_penalty = 10 if is_dry else 0
    score = max(0, min(100, round(100 - (pm25 / 50) * 80 - dry_penalty)))
    return score

def get_score_classification(score):
    """
    Returns score description and visual color key.
    """
    if score >= 75:
        return "Ótimo para sair", "green"
    elif score >= 65:
        return "Bom para sair", "blue"
    elif score >= 55:
        return "Favorável", "yellow"
    elif score >= 45:
        return "Use máscara N95", "orange"
    elif score >= 35:
        return "Use filtro de ar", "orange"
    else:
        return "Evite ou use EPI completo", "red"

def recommend_gear(pm25_pred, no2, rain, month):
    """
    Recommends motorcycle safety gear based on ambient metrics.
    """
    gear = []
    try:
        pm25 = float(pm25_pred)
    except (ValueError, TypeError):
        pm25 = 0.0

    try:
        n2 = float(no2)
    except (ValueError, TypeError):
        n2 = 0.0

    try:
        r = float(rain)
    except (ValueError, TypeError):
        r = 0.0

    try:
        m = int(month)
    except (ValueError, TypeError):
        m = 0

    if pm25 > 12:
        gear.append("🪖 Capacete com filtro de ar — PM2.5 elevado")
    if pm25 > 15:
        gear.append("⚠️ Atenção extra — PM2.5 acima do recomendado pela OMS")
    if pm25 > 25:
        gear.append("😷 Máscara N95 recomendada — nível preocupante")
    if n2 > 40:
        gear.append("🕶️ Viseira fechada — NO2 elevado")
    if r > 5:
        gear.append("🌂 Capa de chuva — precipitação recente")
    if m in [6, 7, 8]:
        gear.append("🧥 Jaqueta com forro — mês mais frio")
        
    if not gear:
        gear = ["✅ Condições favoráveis — equipamento padrão suficiente"]
    return gear

def prepare_features(df_raw):
    """
    Applies feature engineering for XGBoost training and prediction.
    """
    df = df_raw.copy()
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["is_dry"] = (df["month"].between(7, 10)).astype(int)
    
    # Lag and rolling calculations (handling shifts safely)
    df["pm25_lag1"] = df["pm25"].shift(1).fillna(df["pm25"].mean() if "pm25" in df and not df["pm25"].empty else 0)
    df["pm25_lag3"] = df["pm25"].shift(3).fillna(df["pm25"].mean() if "pm25" in df and not df["pm25"].empty else 0)
    df["pm25_roll3"] = df["pm25"].rolling(3, min_periods=1).mean()
    df["rain_acc6"] = df["rain"].rolling(6, min_periods=1).sum() if "rain" in df else 0.0
    return df
