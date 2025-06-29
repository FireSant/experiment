import os
import glob
import logging
import configparser
import shutil # Para mover archivos

from etl_core import ETL
from db_manager import DBManager # Para obtener archivos procesados

# Cargar configuración
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.ini')
config.read(config_path)

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), config['PATHS']['RAW_DATA_DIR'])
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', config['PATHS']['PROCESSED_DATA_DIR'])
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', config['PATHS']['LOG_DIR'])

# Configurar logging para el orquestador
log_file_path = os.path.join(LOG_DIR, 'orchestrator_log.log')
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
logger = logging.getLogger('ETL_Orchestrator')

def run_orchestration():
    """
    Función principal del orquestador.
    Busca nuevos archivos, los procesa y los carga.
    """
    logger.info("Iniciando la orquestación del ETL de averías.")

    # Asegurarse de que los directorios existan
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)
        logger.warning(f"Directorio de datos brutos no encontrado, creado: {RAW_DATA_DIR}")
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)
        logger.warning(f"Directorio de datos procesados no encontrado, creado: {PROCESSED_DATA_DIR}")

    etl_processor = ETL()
    db_manager = DBManager() # Instanciar para acceder a archivos procesados en DB

    # Obtener la lista de archivos ya procesados de la base de datos
    processed_files_in_db = db_manager.get_processed_files()
    logger.info(f"Archivos ya procesados en la DB: {len(processed_files_in_db)}")

    # Buscar archivos en el directorio de entrada (XLSX y CSV)
    # Recursivo=True si los archivos pueden estar en subcarpetas
    raw_files = glob.glob(os.path.join(RAW_DATA_DIR, '**', '*.xlsx'), recursive=True) + \
                glob.glob(os.path.join(RAW_DATA_DIR, '**', '*.csv'), recursive=True)
    
    new_files_to_process = []
    for file_path in raw_files:
        file_name = os.path.basename(file_path)
        # Comprobar si el archivo ya fue procesado y no está en la carpeta processed
        # Podrías también verificar la fecha de modificación del archivo para re-procesar si ha cambiado
        if file_name not in processed_files_in_db:
             new_files_to_process.append(file_path)
        else:
            # Si el archivo está en la DB pero sigue en la carpeta RAW, moverlo.
            # Esto maneja casos donde el ETL falló después de cargar pero antes de mover.
            if os.path.dirname(file_path) == RAW_DATA_DIR: # Solo si está en la carpeta RAW
                etl_processor.move_to_processed(file_path)
                logger.info(f"Archivo '{file_name}' ya en DB, movido a processed.")


    if not new_files_to_process:
        logger.info("No se encontraron nuevos archivos para procesar.")
        return

    logger.info(f"Se encontraron {len(new_files_to_process)} nuevos archivos para procesar.")

    for file_path in new_files_to_process:
        file_name = os.path.basename(file_path)
        logger.info(f"Procesando archivo: {file_name}")
        
        df_raw = etl_processor.extract_data(file_path)
        
        if not df_raw.empty:
            df_transformed = etl_processor.transform_data(df_raw)
            
            if not df_transformed.empty:
                etl_processor.load_data(df_transformed, file_name)
                # Mover el archivo solo si fue exitosamente cargado en la DB
                etl_processor.move_to_processed(file_path)
                logger.info(f"Archivo '{file_name}' procesado y movido exitosamente.")
            else:
                logger.warning(f"Archivo '{file_name}' transformado a DataFrame vacío. No se cargará.")
        else:
            logger.warning(f"Archivo '{file_name}' resultó en DataFrame vacío al extraer. No se procesará.")

    logger.info("Orquestación del ETL finalizada.")

if __name__ == "__main__":
    run_orchestration()