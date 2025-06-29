import pandas as pd
import os
import re # Para expresiones regulares
import logging
import shutil
import configparser
from datetime import datetime

logger = logging.getLogger('ETL_Averias')

# Importar el gestor de la base de datos
from db_manager import DBManager

# Cargar configuración
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'settings.ini')
config.read(config_file_path)

# --- Verificar si el archivo fue leído ---
if not config.sections():
    logger.error(f"ERROR: No se pudo leer el archivo de configuración en {config_file_path}")
    raise FileNotFoundError(f"Archivo de configuración no encontrado o vacío: {config_file_path}")
# --- Fin de la verificación ---

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['PATHS']['RAW_DATA_DIR']) # Ajuste aquí
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['PATHS']['PROCESSED_DATA_DIR']) # Ajuste aquí
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['PATHS']['LOG_DIR']) # Ajuste aquí
EXPECTED_COLUMNS = config['ETL']['EXPECTED_COLUMNS'].split(',')
TEXT_FREE_COLUMNS = config['ETL']['TEXT_FREE_COLUMNS'].split(',')

# Configurar logging para el ETL
log_file_path = os.path.join(LOG_DIR, 'etl_log.log')
# Asegurarse de que el directorio de logs exista
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)


class ETL:
    def __init__(self):
        self.db_manager = DBManager()
        self.db_manager.create_table() # Asegura que la tabla exista al inicializar ETL

    def extract_data(self, file_path: str) -> pd.DataFrame:
        """
        Extrae datos de un archivo XLSX o CSV.
        Maneja columnas esperadas y posibles errores.
        """
        try:
            if file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                logger.warning(f"Formato de archivo no soportado: {file_path}. Saltando.")
                return pd.DataFrame()

            # Asegurarse de que las columnas esperadas estén presentes y en orden
            missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
            if missing_cols:
                logger.error(f"Archivo '{os.path.basename(file_path)}' le faltan columnas esperadas: {missing_cols}")
                return pd.DataFrame()

            df = df[EXPECTED_COLUMNS] # Seleccionar y reordenar columnas
            logger.info(f"Archivo '{os.path.basename(file_path)}' extraído con {len(df)} filas.")
            return df
        except Exception as e:
            logger.error(f"Error al extraer datos de '{os.path.basename(file_path)}': {e}", exc_info=True)
            return pd.DataFrame()

    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma los datos extraídos: limpieza, parsing de texto, cálculo de duraciones.
        """
        if df.empty:
            return pd.DataFrame()

        logger.info("Iniciando transformación de datos.")

        # 1. Copia para no modificar el original (buena práctica)
        df_transformed = df.copy()

        # 2. Conversión de tipos de datos y manejo de nulos en fechas
        df_transformed['Inicio Hora Falla'] = pd.to_datetime(df_transformed['Inicio Hora Falla'], errors='coerce')
        df_transformed['Hora Fin Falla'] = pd.to_datetime(df_transformed['Hora Fin Falla'], errors='coerce')

        # 3. Cálculo de Horas de Parada (en minutos)
        df_transformed['horas_parada_minutos'] = (
            (df_transformed['Hora Fin Falla'] - df_transformed['Inicio Hora Falla']).dt.total_seconds() / 60
        ).fillna(0).astype(int) # Rellenar nulos con 0 y convertir a entero

        # 4. Limpieza y Parsing de la columna 'Novedad' (TEXT_FREE_COLUMNS)
        # Ejemplo de Regex para extraer tipo_averia y componente_afectado
        # Esto es un placeholder; necesitas analizar tus datos reales para definir las regex.
        # Supongamos que Novedad es "Falla de MOTOR X - Componente: Y" o "MANTENIMIENTO PREVENTIVO Grúa A"
        
        df_transformed['tipo_averia_estandar'] = None
        df_transformed['componente_afectado'] = None
        df_transformed['codigo_falla'] = None
        
        # Estandarización básica: minúsculas y eliminación de espacios extra
        df_transformed['Novedad_limpia'] = df_transformed['Novedad'].astype(str).str.lower().str.strip()

        # Regex para tipo de avería (ejemplos muy básicos)
        # Puedes añadir más reglas basadas en tus datos reales.
        # O usar un diccionario de mapeo para palabras clave.
        def classify_novedad(novedad_text):
            if re.search(r'(falla|fallo|daño|averia|problema|error)\s*(de)?\s*(motor|bomba|sistema)', novedad_text):
                return 'Falla de Equipo Principal'
            if re.search(r'mantenimiento\s*(preventivo|correctivo)', novedad_text):
                return 'Mantenimiento'
            if re.search(r'(inspeccion|revision)\s*(rutinaria)?', novedad_text):
                return 'Inspección/Revisión'
            # Añade más reglas...
            return 'Otros/Desconocido'

        df_transformed['tipo_averia_estandar'] = df_transformed['Novedad_limpia'].apply(classify_novedad)
        
        # Regex para componente afectado (ejemplos)
        # pattern_componente = r'(motor|bomba|cable|eje|válvula|sistema hidráulico)'
        # df_transformed['componente_afectado'] = df_transformed['Novedad_limpia'].str.extract(pattern_componente, flags=re.IGNORECASE)[0].str.capitalize()
        
        # Para detección de códigos de falla (ej. "COD:XYZ" o "Error: 123")
        # pattern_codigo = r'(cod|code|error|err)[:\s-]?(\w+-\d+|\d{3,})'
        # df_transformed['codigo_falla'] = df_transformed['Novedad_limpia'].str.extract(pattern_codigo, flags=re.IGNORECASE)[1]


        # 5. Manejo general de nulos para otras columnas importantes
        # Rellenar con "Desconocido" o valores por defecto.
        df_transformed['Sistema Afectado'] = df_transformed['Sistema Afectado'].fillna('Desconocido')
        df_transformed['Buque'] = df_transformed['Buque'].fillna('N/A')
        df_transformed['Equipo'] = df_transformed['Equipo'].fillna('N/A')

        logger.info("Transformación de datos completada.")
        return df_transformed[['Equipo', 'Novedad', 'Inicio Hora Falla', 'Hora Fin Falla', 
                               'horas_parada_minutos', 'Sistema Afectado', 'Buque',
                               'tipo_averia_estandar', 'componente_afectado', 'codigo_falla']]

    def load_data(self, df: pd.DataFrame, filename: str):
        """
        Carga el DataFrame transformado en la base de datos SQLite.
        """
        if df.empty:
            logger.warning(f"No hay datos para cargar del archivo '{filename}'.")
            return
        
        logger.info(f"Cargando datos del archivo '{filename}' en la base de datos.")
        self.db_manager.insert_data(df, filename)
        logger.info(f"Datos del archivo '{filename}' cargados exitosamente.")

    def move_to_processed(self, file_path: str):
        """Mueve un archivo procesado a la carpeta de procesados."""
        try:
            if not os.path.exists(PROCESSED_DATA_DIR):
                os.makedirs(PROCESSED_DATA_DIR)
            shutil.move(file_path, os.path.join(PROCESSED_DATA_DIR, os.path.basename(file_path)))
            logger.info(f"Archivo '{os.path.basename(file_path)}' movido a '{PROCESSED_DATA_DIR}'.")
        except Exception as e:
            logger.error(f"Error al mover archivo '{os.path.basename(file_path)}': {e}", exc_info=True)