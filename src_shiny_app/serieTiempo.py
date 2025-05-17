import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

def serieTiempo(df, selected_month, year_start, year_end, selected_vehicle):
    
    warnings.filterwarnings("ignore", category=UserWarning, module="statsmodels")
    warnings.filterwarnings("ignore", category=FutureWarning, module="statsmodels")

    meses_dict = {
        "ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4,
        "MAYO": 5, "JUNIO": 6, "JULIO": 7, "AGOSTO": 8,
        "SEPTIEMBRE": 9, "OCTUBRE": 10, "NOVIEMBRE": 11, "DICIEMBRE": 12
    }
    
    month_num = meses_dict[selected_month]
    
    df_filtered = df[(df["AÑO"] >= year_start) & (df["AÑO"] <= year_end)].copy()
    
    if selected_vehicle not in df_filtered.columns:
        raise ValueError("La columna seleccionada no existe en los datos.")
    
    df_filtered[selected_vehicle] = (
        df_filtered[selected_vehicle]
        .astype(str)
        .str.replace(",", "")
        .str.strip()
        .replace("", "0")
        .astype(float)
    )
    
    df_grouped = df_filtered.groupby(["AÑO", "MES"])[selected_vehicle].sum().reset_index()
    
    df_grouped["MES_NUM"] = df_grouped["MES"].map(meses_dict)
    df_grouped["FECHA"] = pd.to_datetime(df_grouped["AÑO"].astype(str) + "-" + df_grouped["MES_NUM"].astype(str) + "-01")
    df_grouped = df_grouped.sort_values("FECHA")
    
    ts = df_grouped.set_index("FECHA")[selected_vehicle]
    
    if len(ts) < 12:
        raise ValueError("No hay suficientes datos para pronosticar. Se requieren al menos 12 meses de datos.")

    model = SARIMAX(ts, order=(1, 0, 1), seasonal_order=(1, 1, 1, 12), enforce_stationarity=False, enforce_invertibility=False) 
    model_fit = model.fit(disp=False)

    # Visualización
    plt.figure(figsize=(6, 2))
    plt.plot(ts, label="Datos históricos", color="black")
    plt.axvline(ts.index[-1], color="gray", linestyle="--", label="Límite de pronóstico")

    forecast_dates = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=1), periods=12, freq='MS')
    forecast = model_fit.get_forecast(steps=12)
    forecast_values = forecast.predicted_mean

    # Línea de predicción
    # forecast_dates = pd.date_range(start=ts.index[-1], periods=12, freq='MS')
    plt.plot(forecast_dates, forecast_values, color="blue", linestyle="--", label="Pronóstico")
    mask = forecast_dates.month == month_num
    forecast_value_selected = None
    if mask.any():
        forecast_value_selected = forecast_values[mask].iloc[0]
        plt.plot(forecast_dates[mask], forecast_value_selected, 'ro', markersize=8, 
                label=f'Pronóstico {selected_month}: {forecast_value_selected:,.0f}')
    
    plt.title(f"Pronóstico para {selected_vehicle} ({selected_month})")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad total")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout(pad=0.1)
    plt.subplots_adjust(top=0.925, bottom=0.18, left=0.15, right=0.98)
    plt.xticks(fontsize=8)
    return plt.gcf(), forecast_value_selected
