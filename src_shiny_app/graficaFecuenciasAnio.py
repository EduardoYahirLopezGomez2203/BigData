import pandas as pd
import matplotlib.pyplot as plt

def generarGraficaFrecuencia(datos, vehiculos, anio_especifico):
    
    datos_filtrados = datos[datos['AÑO'] == anio_especifico].copy()

    frecuencias = {}
    for vehiculo in vehiculos:
        if vehiculo in datos_filtrados.columns:
            # Usamos .loc para modificar la copia de forma segura
            # datos_filtrados.loc[:, vehiculo] = datos_filtrados[vehiculo].astype(str).str.replace(',', '')
            # datos_filtrados.loc[:, vehiculo] = pd.to_numeric(datos_filtrados[vehiculo], errors='coerce').fillna(0)
            datos_filtrados[vehiculo] = pd.to_numeric(datos_filtrados[vehiculo].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)
            frecuencias[vehiculo] = datos_filtrados[vehiculo].mean()
        else:
            print(f"Advertencia: El tipo de vehículo '{vehiculo}' no existe en los datos.")

    print(frecuencias)

    # Colores predeterminados para cada vehículo
    colores = {
        'AUTOS': 'blue',
        'MOTOS': 'red',
        'AUTOBUS DE 2 EJES': 'green',
        'AUTOBUS DE 3 EJES': 'yellow',
        'AUTOBUS DE 4 EJES': 'pink'
    }

    colores_barras = [colores.get(v, 'gray') for v in frecuencias.keys()]

    plt.figure(figsize=(4, 10))

    barras = plt.bar(frecuencias.keys(), frecuencias.values(), color=colores_barras, width=0.2)

    plt.title(f'Frecuencia de tipos de vehículo en el año {anio_especifico}')
    plt.xlabel('Tipo de vehículo')
    plt.ylabel('Cantidad')

    # Agregar etiquetas con valor exacto encima de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # posición horizontal: centro de la barra
            altura,                                # posición vertical: justo encima de la barra
            f'{int(altura):,}',                    # valor exacto, con separador de miles
            ha='center',                          # alineación horizontal centrada
            va='bottom',                          # alineación vertical abajo (justo encima)
            fontsize=9,
            rotation=0
        )

    plt.xticks(ha='right', fontsize=6)
    plt.tight_layout(pad=0.1)
    plt.subplots_adjust(top=0.925, bottom=0.18, left=0.15, right=0.98)
    if len(frecuencias) == 1:
        plt.xlim(-0.5, 0.5)
        
    return plt.gcf()


