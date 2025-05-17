from shiny import App, Inputs, Outputs, Session, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from serieTiempo import serieTiempo
from graficaFecuenciasAnio import generarGraficaFrecuencia
import requests
from io import StringIO
from datos_csv import load_csv


def load_csv_from_drive():
    
        return load_csv()
    
icons = {
            "AUTOS": "🚗",
            "MOTOS": "🏍️",
            "AUTOBUS DE 2 EJES": "🚌",
            "AUTOBUS DE 3 EJES": "🚌",
            "AUTOBUS DE 4 EJES": "🚌"
}

app_ui = ui.page_fluid(
    ui.row(
        
        ui.column(
            2,
            ui.input_slider("time_period", "Período de tiempo", min=2021, max=2025, value=2022),
            ui.input_select("select_option", "Seleccionar tipo:", {
                "AUTOS": "AUTOS", "MOTOS": "MOTOS", "AUTOBUS DE 2 EJES": "AUTOBUS DE 2 EJES", "AUTOBUS DE 3 EJES": "AUTOBUS DE 3 EJES", "AUTOBUS DE 4 EJES": "AUTOBUS DE 4 EJES"
            }),
            ui.input_select("select_mes", "Meses:", {
                "ENERO": "ENERO", "FEBRERO": "FEBRERO", "MARZO": "MARZO", "ABRIL": "ABRIL", "MAYO": "MAYO",
                "JUNIO": "JUNIO", "JULIO": "JULIO", "AGOSTO": "AGOSTO", "SEPTIEMBRE": "SEPTIEMBRE",
                "OCTUBRE": "OCTUBRE", "NOVIEMBRE": "NOVIEMBRE", "DICIEMBRE": "DICIEMBRE"
            }),
            ui.div(style="height: 340px;"),
            ui.input_select("select_anio", "Seleccionar Año:", {
                "2021": 2021, "2022": 2022, "2023": 2023, "2024": 2024, "2025": 2025,
            }),
            ui.input_checkbox("Autos", "AUTOS", True),
            ui.input_checkbox("Motos", "MOTOS", False),
            ui.input_checkbox("Autobus2", "AUTOBUS DE 2 EJES", False),
            ui.input_checkbox("Autobus3", "AUTOBUS DE 3 EJES", False),
            ui.input_checkbox("Autobus4", "AUTOBUS DE 4 EJES", False),
             style="margin-top: 20px; padding: 0px 20px 20px 20px"
        ),
        
        
        
        ui.column(
            10,
            # Fila horizontal para los 3 elementos
            ui.row(
                ui.column(
                    4,
                    ui.row(
                            ui.div(
                                ui.output_text("total_vehicle_icon"),
                                style="font-size: 40px; text-align: left; margin: 0;"
                            ),
                            ui.div(
                                ui.output_text("text_vehicle"),
                                style="margin: 0; font-size: 14px; color: #003366;"
                            ),
                            ui.div(
                                ui.output_text("total_vehicle"),
                                style="margin: 0; font-size: 24px; font-weight: bold; color: #000;" 
                            )
                        )
                ),
                # Columna para Motos
                ui.column(
                    4,
                    ui.row(
                        ui.span("📅", style="font-size: 40px; width: 60px; display: inline-block; text-align: center;"),
                        ui.div(
                                ui.h4("Frecuencia del mes de:", style="margin: 0; font-size: 14px; color: #003366;"),
                                ui.output_text("frecuency"),
                                style="margin: 0; font-size: 24px; font-weight: bold; color: #000;" 
                        )
                    ),
                    style="display: flex; align-items: center; margin-bottom: 10px; border-right: 1px solid #eee; padding-right: 15px;"
                ),
                # Columna para Autobuses
                ui.column(
                    4,
                    ui.row(
                        ui.div(
                                ui.output_text("total_vehicle_pronostic_icon"),  # Ícono dinámico
                                style="font-size: 40px; text-align: left; margin: 0;"  # Estilo aplicado al contenedor
                        ),
                        ui.div(
                                ui.output_text("text_pronostic"),  # Ícono dinámico
                                style="margin: 0; font-size: 14px; color: #003366;"
                        ),
                        ui.div(
                                ui.output_text("pronostic"),
                                style="margin: 0; font-size: 24px; font-weight: bold; color: #000;" 
                        )
                    ),
                    style="display: flex; align-items: center; margin-bottom: 10px;"
                ),
                style="display: flex; justify-content: space-between; margin-bottom: 20px; margin-top: 20px; margin-right: 5px; background-color: #fff; border: 1px solid #ccc;border-radius: 10px;"
            ),
            ui.row(
                ui.column(
                    4,
                    ui.div(
                        ui.h2("Conjunto de Datos", style="font-size: 18px;  font-weight: bold;"),
                        ui.div(
                                ui.output_table("csv_table"),
                                style="""
                                    max-height: 300px;
                                    overflow-y: scroll;
                                    border: 2px solid #ccc;
                                    width: 100%;
                                    font-size: 12px;
                                    background: #fff;
                                """
                            ),
                            ui.tags.style("""
                                #csv_table th, #csv_table td {
                                    border: 1px solid #000;
                                    padding: 0px 0px 0px 70px;
                                    text-align: center;
                                }
                                #csv_table th {
                                    background-color: #003366;
                                    color: #fff;
                                }
                            """),
                    )
                ),
                ui.column(
                    7,
                        ui.output_plot("forecast_plot"),
                ),
                 style="display: flex; justify-content: center; margin-bottom: 20px; margin-right: 5px; background-color: #fff; border: 1px solid #ccc;border-radius: 10px; padding-top: 20px;"
            ), 
            ui.row(
                ui.column(
                        6,
                        ui.output_plot("frecuency_plot"),
                ),
                ui.column(
                        3,
                        ui.h2("Cantidad de vehiculos", style="font-size: 18px; font-weight: bold;"),
                        ui.output_ui("resumen_vehiculos"),
                ),
                ui.column(
                        3,
                        ui.h2("Estadísticas", style="font-size: 18px; font-weight: bold;"),
                        ui.output_ui("estadisticas"),
                        
                ),
                 style="display: flex; justify-content: space-between; margin-bottom: 20px; margin-right: 5px; background-color: #fff; border: 1px solid #ccc;border-radius: 10px; padding-top: 20px;"
            ) 
        )
    ),
)



def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def get_data():
        if not hasattr(session, "cached_df"):
            print("Descargando y cacheando datos...")
            session.cached_df = load_csv_from_drive()
        return session.cached_df
    
    @render.table
    def csv_table():
        df = get_data()
        year_start = 2021
        year_end = input.time_period()
        selected_month = input.select_mes()
        selected_vehicle = input.select_option()

        df_filtered = df[(df["AÑO"] >= year_start) & (df["AÑO"] <= year_end) & (df["MES"] == selected_month)]
        if selected_vehicle in df_filtered.columns:
            return df_filtered[["AÑO", "MES", selected_vehicle]]
        else:
            return pd.DataFrame({"Error": ["La columna seleccionada no existe en los datos."]})

    @render.plot
    def forecast_plot():
        year_start = 2021
        year_end = input.time_period()
        selected_month = input.select_mes()
        selected_vehicle = input.select_option()

        fig,_ = serieTiempo(get_data(), selected_month, year_start, year_end, selected_vehicle)
        return fig
    
    @render.text
    def total_vehicle_icon():
        return icons.get(input.select_option(), "❓")
    
    @render.text
    def text_vehicle():
        
        selected_option = "Total de " + input.select_option() + " hasta " + str(input.time_period())
        
        return selected_option
    
    @render.text
    def total_vehicle():
        df = get_data()
        year_start = 2021
        year_end = input.time_period()
        selected_month = input.select_mes()
        selected_vehicle = input.select_option()

        # Filtra solo por año
        df_filtered = df[(df["AÑO"] >= year_start) & (df["AÑO"] <= year_end) & (df["MES"] == selected_month)]

        if selected_vehicle in df_filtered.columns:
            # Elimina comas y convierte a numérico
            total = pd.to_numeric(df_filtered[selected_vehicle].astype(str).str.replace(',', ''), errors="coerce").sum()
            return f"{total:,.0f}"
        else:
            return "N/A"
        
    @render.text
    def frecuency():
        selected_month = input.select_mes()
        return selected_month
    
    @render.text
    def total_vehicle_pronostic_icon():
        
        return icons.get(input.select_option(), "❓")
    
    @render.text
    def text_pronostic():
        
        selected_option = "Pronostico para el mes de " + input.select_mes() + " del año " + str(input.time_period() + 1)
        
        return selected_option
    
    @render.text
    def pronostic():
        
        year_start = 2021
        year_end = input.time_period()
        selected_month = input.select_mes()
        selected_vehicle = input.select_option()

        _,forecast_value = serieTiempo(get_data(),selected_month, year_start, year_end, selected_vehicle)
        return f"{forecast_value:,.0f}"
    
    @render.plot
    def frecuency_plot():
        selected_year = int(input.select_anio())
        vehicles = []
        if input.Autos():
            vehicles.append("AUTOS")
        if input.Motos():
            vehicles.append("MOTOS")
        if input.Autobus2():
            vehicles.append("AUTOBUS DE 2 EJES")
        if input.Autobus3():
            vehicles.append("AUTOBUS DE 3 EJES")
        if input.Autobus4():
            vehicles.append("AUTOBUS DE 4 EJES")
            
        fig = generarGraficaFrecuencia(get_data(), vehicles, selected_year)
        return fig
    
    @render.ui
    def resumen_vehiculos():
        df = get_data()
        selected_year = int(input.select_anio())
        vehiculos = []
        if input.Autos():
            vehiculos.append("AUTOS")
        if input.Motos():
            vehiculos.append("MOTOS")
        if input.Autobus2():
            vehiculos.append("AUTOBUS DE 2 EJES")
        if input.Autobus3():
            vehiculos.append("AUTOBUS DE 3 EJES")
        if input.Autobus4():
            vehiculos.append("AUTOBUS DE 4 EJES")    
            
        items = []
        for v in vehiculos:
            icono = icons.get(v, "❓")
            if v in df.columns:
                total = pd.to_numeric(
                    df[df["AÑO"] == selected_year][v].astype(str).str.replace(',', ''),
                    errors="coerce"
                ).sum()
                total_str = f"{total:,.0f}"
            else:
                total_str = "N/A"
            items.append(
                ui.div(
                    ui.span(icono, style="font-size: 30px; margin-right: 8px;"),
                    ui.span(v+": ", style="font-weight: bold; margin-right: 0px; font-size: 14px;"),
                    ui.span(total_str, style="color: #003366; font-size: 14px;"),
                    style="margin-bottom: 10px;"
                )
            )
        if not items:
            items.append(ui.div("No hay vehículos seleccionados."))
        return ui.div(*items)
    
    @render.ui
    def estadisticas():
        selected_year = int(input.select_anio())
        vehiculos = []
        if input.Autos():
            vehiculos.append("AUTOS")
        if input.Motos():
            vehiculos.append("MOTOS")
        if input.Autobus2():
            vehiculos.append("AUTOBUS DE 2 EJES")
        if input.Autobus3():
            vehiculos.append("AUTOBUS DE 3 EJES")
        if input.Autobus4():
            vehiculos.append("AUTOBUS DE 4 EJES")  
        
        datos = get_data()
        datos_filtrados = datos[datos['AÑO'] == selected_year].copy()

        frecuencias = {}
        for vehiculo in vehiculos:
            if vehiculo in datos_filtrados.columns:
                # Usamos .loc para modificar la copia de forma segura
                # datos_filtrados.loc[:, vehiculo] = datos_filtrados[vehiculo].astype(str).str.replace(',', '')
                # datos_filtrados.loc[:, vehiculo] = pd.to_numeric(datos_filtrados[vehiculo], errors='coerce').fillna(0)
                datos_filtrados[vehiculo] = pd.to_numeric(datos_filtrados[vehiculo].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)
                frecuencias[vehiculo] = datos_filtrados[vehiculo].mean()
            else:
                frecuencias[vehiculo] = None
                
        items = []
        if frecuencias:
            # Filtra solo los que tienen datos válidos
            frecuencias_validas = {k: v for k, v in frecuencias.items() if v is not None}
            if frecuencias_validas:
                mayor = max(frecuencias_validas, key=frecuencias_validas.get)
                items.append(
                    ui.div(
                        ui.span("Tipo de vehiculo con mayor movimiento: ", style="color: black; font-weight: bold;"),
                        ui.span(f"{mayor}", style="color: green; font-weight: bold;"),
                        style="margin-bottom: 8px;"
                    )
                )
                if len(frecuencias_validas) > 1:
                    menor = min(frecuencias_validas, key=frecuencias_validas.get)
                    if menor != mayor:
                        items.append(
                            ui.div(
                                ui.span("Tipo de vehiculo con menor movimiento: ", style="color: black; font-weight: bold;"),
                                ui.span(f"{menor}", style="color: red; font-weight: bold;"),
                                style="margin-bottom: 8px;"
                            )
                        )
        if not items:
            items.append(ui.div("No hay datos suficientes para calcular estadísticas."))
        return ui.div(*items)
    
app = App(app_ui, server)
