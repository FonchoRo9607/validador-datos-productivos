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

```
validador-datos-productivos/
│── validador_datos.py        # Script principal / Main script
│── reglas.json               # Reglas configurables / Configurable rules
│── requirements.txt          # Dependencias / Dependencies
│── assets/
│    └── logo.png             # Logo opcional / Optional logo
│── README.md                 # Documentación / Documentation
```
---

## ⚙️ Instalación local / Local installation

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/FonchoRo9607/validador-datos-productivos.git
   cd validador-datos-productivos
---
2. Crear entorno virtual e instalar dependencias:
   ```
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   
   ```
---
3. Ejecutar la aplicación:

   ```
   streamlit run validador_datos.py

   ```
---  

4. Abrir el navegador/Open in browser:

   ```
   http://localhost:8501
   ```
---

# Despliegue en Streamlit Cloud / Deployment on Streamlit Cloud

   ```
   - Conecta tu cuenta de GitHub en Streamlit Cloud.
   - Selecciona el repositorio validador-datos-productivos.
   - Define el archivo principal: validador_datos.py.
   - Streamlit instalará automáticamente las dependencias de requirements.txt.
   - Tu aplicación quedará disponible en una URL pública / Your app will be available at a public URL.
   ```
---

# Ejemplos de reglas/Example rules (reglas.json)

   ```
   {
     "columnas_obligatorias": ["id", "fecha", "valor"],
     "unicidad": ["id"],
     "rangos": {
       "valor": { "min": 0, "max": 100 }
     },
     "fechas_validas": {
       "fecha": { "min": "2020-01-01", "max": "2025-12-31" }
     }
   }

   ```
---

# Tecnologías/Technologies

   ```
   - Python 3.9+
   - Streamlit
   - Pandas
   - Matplotlib
   - Seaborn
   - fpdf2

   ```
---

# Autor / Author

## Alfonso Romero Martínez

Ingeniero Informático | Backend Developer | Data Scientist | Arquitecto de Software en formación
