# Validador de Datos Productivos / Productive Data Validator

Aplicación en **Python + Streamlit** que permite validar archivos CSV según reglas configurables, generar gráficos de calidad de datos y exportar un informe bilingüe (Español/Inglés) en PDF.  
El proyecto está diseñado para ser **portable**, funcionando tanto en local como en la nube (Streamlit Cloud), sin dependencias externas como `wkhtmltopdf`.

---

## 🚀 Características / Features

- ✅ Validación de columnas obligatorias  
- ✅ Detección de duplicados y valores nulos  
- ✅ Verificación de rangos numéricos y fechas válidas  
- ✅ Identificación de tipos de datos  
- ✅ Generación de gráficos con **Matplotlib/Seaborn**  
- ✅ Exportación de informe PDF bilingüe con **fpdf2**  
- ✅ Interfaz web interactiva con **Streamlit**  
- ✅ Botón de descarga del informe directamente desde la aplicación  

---

## 📂 Estructura del proyecto / Project structure
validador-datos-productivos/
│── validador_datos.py        # Script principal / Main script
│── reglas.json               # Reglas configurables / Configurable rules
│── requirements.txt          # Dependencias / Dependencies
│── assets/
│    └── logo.png             # Logo opcional / Optional logo
│── README.md                 # Documentación / Documentation

---
