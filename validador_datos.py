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



def generar_informe(resultados, rutas_graficos=None, nombre_archivo="informe_validacion.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)

    # Título
    pdf.cell(200, 10, txt="Informe de Validación de Datos / Data Validation Report", ln=True, align="C")
    pdf.ln(10)

    # Resumen
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total de registros / Total records: {resultados.get('total_registros', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Columnas faltantes / Missing columns: {resultados.get('columnas_faltantes', [])}", ln=True)
    pdf.ln(10)

    # Duplicados
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Duplicados / Duplicates", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in resultados.items():
        if "duplicados" in k:
            pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    pdf.ln(5)

    # Valores nulos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Valores nulos / Null values", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in resultados.get("nulos", {}).items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    pdf.ln(5)

    # Tipos de datos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Tipos de datos detectados / Detected data types", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in resultados.get("tipos_detectados", {}).items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    pdf.ln(10)

    # Gráficos incrustados
    if rutas_graficos:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Gráficos / Charts", ln=True)
        pdf.ln(5)
        for ruta in rutas_graficos:
            pdf.image(ruta, x=10, w=180)
            pdf.ln(10)

    # Guardar PDF
    pdf.output(nombre_archivo)
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












