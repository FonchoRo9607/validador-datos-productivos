# Proyecto validador de datos
# Versión 0.01
# Autor: Alfonso Javier Romero Martínez 

# 1. Importamos las librerías Pandas y StreamLit

import pandas as pd
import streamlit as st
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from fpdf import FPDF





## Cargar los datos

def cargar_datos(archivo):
    try:
        df = pd.read_csv(archivo)
        return df
    except Exception as e:
        st.error(f"Error al cargar archivo: {e}")
        return None
## Cargar las reglas definidas en JSON.

def cargar_reglas(path="reglas.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:  # aseguramos UTF-8
            reglas = json.load(f)
        return reglas
    except Exception as e:
        st.error(f"Error al cargar reglas: {e}")
        return {}






## validaciones de datos

def validar_datos(df, reglas):
    resultados = {}

    # Columnas obligatorias
    faltantes = [col for col in reglas.get("columnas_obligatorias", []) if col not in df.columns]
    resultados["columnas_faltantes"] = faltantes

    # Unicidad
    for col in reglas.get("unicidad", []):
        if col in df.columns:
            resultados[f"duplicados_{col}"] = df[col].duplicated().sum()

    # Tipos de datos
    resultados["tipos_detectados"] = df.dtypes.astype(str).to_dict()

    # Rangos
    for col, limites in reglas.get("rangos", {}).items():
        if col in df.columns:
            fuera_rango = df[(df[col] < limites["min"]) | (df[col] > limites["max"])]
            resultados[f"fuera_rango_{col}"] = len(fuera_rango)

    # Fechas válidas
    for col, limites in reglas.get("fechas_validas", {}).items():
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            fuera_fecha = df[(df[col] < datetime.fromisoformat(limites["min"])) |
                             (df[col] > datetime.fromisoformat(limites["max"]))]
            resultados[f"fuera_fecha_{col}"] = len(fuera_fecha)

    # Valores nulos
    resultados["nulos"] = df.isnull().sum().to_dict()

    resultados["total_registros"] = len(df)
    return resultados





## Generar gráficos y guardarlos


def generar_graficos(resultados, mostrar=True):
    rutas = []

    # Gráfico de nulos
    nulos_filtrados = {col: val for col, val in resultados["nulos"].items() if val > 0}
    if nulos_filtrados:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=list(nulos_filtrados.keys()), y=list(nulos_filtrados.values()), ax=ax, palette="Blues_d")
        ax.set_title("Valores nulos por columna / Null values per column")
        plt.xticks(rotation=45, ha="right", fontsize=9)
        ruta_nulos = os.path.abspath("grafico_nulos.png")
        fig.savefig(ruta_nulos, bbox_inches="tight")
        rutas.append(ruta_nulos)
        if mostrar:
            st.pyplot(fig)
        plt.close(fig)

    # Gráfico de duplicados
    if "duplicados_id" in resultados:
        duplicados = resultados["duplicados_id"]
        total = resultados["total_registros"]
        validos = total - duplicados
        fig, ax = plt.subplots()
        ax.pie([validos, duplicados], labels=["Válidos / Valid", "Duplicados / Duplicates"], autopct="%1.1f%%",
               colors=["lightgreen", "salmon"])
        ax.set_title("Proporción de registros válidos vs duplicados / Valid vs duplicate records")
        ruta_dup = os.path.abspath("grafico_duplicados.png")
        fig.savefig(ruta_dup, bbox_inches="tight")
        rutas.append(ruta_dup)
        if mostrar:
            st.pyplot(fig)
        plt.close(fig)

    return rutas








## Generar Informe



def generar_informe(resultados, nombre_archivo="informe_validacion.pdf"):
    rutas_graficos = generar_graficos(resultados, mostrar=False)
    ruta_logo = os.path.abspath("logo.png")  # opcional, tu logo personal

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Informe de Validación / Validation Report</title>
        <style>
            body {{ font-family: Arial, Helvetica, sans-serif; margin: 40px; }}
            header {{ display: flex; align-items: center; margin-bottom: 20px; }}
            header img {{ height: 60px; margin-right: 20px; }}
            header h1 {{ color: #2c3e50; }}
            h2 {{ color: #2980b9; margin-top: 30px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 15px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #2980b9; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .summary {{ background-color: #ecf0f1; padding: 10px; margin-bottom: 20px; }}
            img.chart {{ max-width: 600px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <header>
            <img src="{ruta_logo}" alt="Logo"/>
            <h1>Informe de Validación de Datos / Data Validation Report</h1>
        </header>

        <div class="summary">
            <p><strong>Total de registros / Total records:</strong> {resultados.get('total_registros', 'N/A')}</p>
            <p><strong>Columnas faltantes / Missing columns:</strong> {resultados.get('columnas_faltantes', [])}</p>
        </div>

        <h2>Duplicados / Duplicates</h2>
        <table>
            <tr><th>Columna / Column</th><th>Cantidad / Count</th></tr>
            {"".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in resultados.items() if "duplicados" in k])}
        </table>

        <h2>Valores nulos / Null values</h2>
        <table>
            <tr><th>Columna / Column</th><th>Cantidad / Count</th></tr>
            {"".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in resultados.get('nulos', {}).items()])}
        </table>

        <h2>Tipos de datos detectados / Detected data types</h2>
        <table>
            <tr><th>Columna / Column</th><th>Tipo / Type</th></tr>
            {"".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in resultados.get('tipos_detectados', {}).items()])}
        </table>

        <h2>Gráficos / Charts</h2>
        {"".join([f"<img class='chart' src='{ruta}' />" for ruta in rutas_graficos])}
    </body>
    </html>
    """

    config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    options = {"enable-local-file-access": None, "encoding": "UTF-8"}

    pdfkit.from_string(html_content, nombre_archivo, configuration=config, options=options)
    return nombre_archivo









## interfaz

def main():
    st.title("Validador de Datos Productivos con Informe Bilingüe (UTF-8)")
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    reglas = cargar_reglas()

    if archivo is not None:
        df = pd.read_csv(archivo, encoding="utf-8")  # aseguramos lectura en UTF-8
        st.write("Vista previa de los datos / Data preview:")
        st.dataframe(df.head())

        resultados = validar_datos(df, reglas)

        st.subheader("Resultados de validación / Validation results")
        st.json(resultados)

        st.subheader("Gráficos en la interfaz / Charts in interface")
        generar_graficos(resultados, mostrar=True)

        if st.button("Generar Informe PDF Bilingüe"):
            archivo_pdf = generar_informe(resultados)
            st.success(f"Informe generado: {archivo_pdf}")

if __name__ == "__main__":
    main()












