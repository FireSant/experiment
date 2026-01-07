import os
from dotenv import load_dotenv
from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine

# Cargar las variables de entorno del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE LA BASE DE DATOS (leída desde el entorno) ---
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Validar que todas las variables fueron cargadas
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Faltan una o más variables de entorno para la base de datos en el archivo .env")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)
engine = create_engine(DATABASE_URL)

@app.route('/')
def index():
    try:
        df = pd.read_sql_query("SELECT * FROM costos_productos_final", engine)
        df = df.round(2)
        tabla_html = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', tabla=tabla_html)
    except Exception as e:
        return f"Error al cargar los datos: {e}. Asegúrate de haber ejecutado el pipeline ETL primero."

if __name__ == '__main__':
    app.run(debug=True, port=5001)