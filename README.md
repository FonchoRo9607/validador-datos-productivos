# Validador de Datos Productivos / Productive Data Validator

## Descripción / Description
Este proyecto es una aplicación en **Python + Streamlit** que permite validar datos productivos según reglas configurables, generar visualizaciones y exportar informes en **PDF bilingüe (Español/Inglés)** con tablas y gráficos incrustados.  
This project is a **Python + Streamlit** application that validates productive data based on configurable rules, generates visualizations, and exports **bilingual PDF reports (Spanish/English)** with embedded tables and charts.

---

Características / Features
- Validación de columnas obligatorias / Mandatory column validation  
- Detección de duplicados y valores nulos / Duplicate and null value detection  
- Verificación de rangos y fechas válidas / Range and date validation  
- Visualizaciones interactivas en Streamlit / Interactive visualizations in Streamlit  
- Exportación de informes PDF bilingües con gráficos / Bilingual PDF report export with charts  
- Personalización con logo o encabezado / Customizable with logo or header  

---

##  Instalación / Installation
1. Clona este repositorio / Clone this repository:
   ```bash
   git clone https://github.com/TU_USUARIO/validador-datos-productivos.git
   cd validador-datos-productivos
2. Crea un entorno virtual e instala dependencias / Create a virtual environment and install dependencies:
   ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
    pip install -r requirements.txt
  
4. Uso/Usage:
   
   Ejecuta la aplicación con Streamlit / Run the app with Streamlit:
   ```bash
   streamlit run validador_datos.py

Sube tu archivo CSV y genera el informe PDF bilingüe con un clic.
Upload your CSV file and generate the bilingual PDF report with one click
   

Estructura del proyecto / Project structure:

validador-datos-productivos/

│── validador_datos.py        # Script principal / Main script
│── reglas.json               # Reglas configurables / Configurable rules
│── requirements.txt          # Dependencias / Dependencies
│── assets/
│    └── logo.png             # Logo opcional / Optional logo
│── README.md                 # Documentación / Documentation


Autor / Author
Alfonso Romero Martínez
Ingeniero Informático | Python & Machine Learning | Data Science | Backend Development

Licencia / License
Este proyecto está bajo la licencia MIT.
This project is licensed under the MIT License.














