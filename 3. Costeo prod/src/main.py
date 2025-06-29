from sqlalchemy import create_engine
from etl.pipeline import extract_data, transform_data, load_data
from dotenv import load_dotenv
import os

# La forma más robusta para TU estructura:
# Asumimos que main.py está en src/ y .env está en la raíz de proyecto_costeo/
# project_root será la ruta hasta 'proyecto_costeo'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Sube un nivel de 'src' a 'proyecto_costeo'
dotenv_path = os.path.join(project_root, '.env')

# Cargar las variables de entorno desde la ruta específica
load_dotenv(dotenv_path)

# --- CONFIGURACIÓN DE LA BASE DE DATOS (leída desde el entorno) ---
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Validar que todas las variables fueron cargadas
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("Error: Faltan una o más variables de entorno para la base de datos.")
    exit()

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- CONFIGURACIÓN DE SALIDA CSV ---
OUTPUT_CSV_FILENAME = 'costos_productos_final.csv'
# Guardar en la carpeta 'data/' de la raíz del proyecto
OUTPUT_CSV_PATH = os.path.join(project_root, 'data','procesado', OUTPUT_CSV_FILENAME)


def main():
    """Función principal para ejecutar el pipeline ETL completo."""
    # Crear conexión a la base de datos
    try:
        engine = create_engine(DATABASE_URL)
        # Probar conexión
        engine.connect()
    except Exception as e:
        print(f"No se pudo conectar a la base de datos: {e}")
        return

# Ejecutar ETL
    data = extract_data()
    if data:
        transformed_df = transform_data(*data)
        # Llamar a load_data pasando la ruta del CSV
        load_data(transformed_df, engine, output_csv_path=OUTPUT_CSV_PATH)
    else:
        print("No se pudo extraer datos, el pipeline no continuará.")

if __name__ == '__main__':
    main()