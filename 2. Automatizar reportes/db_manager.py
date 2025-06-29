import sqlite3
import pandas as pd
import os
import configparser

# Cargar configuración
config = configparser.ConfigParser()
# La ruta correcta para settings.ini desde db_manager.py
# Si db_manager.py está en la raíz del proyecto y config/settings.ini está dentro de 'config'
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'settings.ini')
config.read(config_file_path)

# --- Verificar si el archivo fue leído ---
if not config.sections():
    print(f"ERROR: No se pudo leer el archivo de configuración en {config_file_path}")
    print("Asegúrate de que la ruta es correcta y el archivo settings.ini existe y no está vacío.")
    # Considera levantar una excepción aquí para detener el programa
    raise FileNotFoundError(f"Archivo de configuración no encontrado o vacío: {config_file_path}")
# --- Fin de la verificación ---


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['PATHS']['DB_PATH']) # Esto también necesita ajuste
TABLE_NAME = config['DATABASE']['TABLE_NAME']

class DBManager:
    def __init__(self, db_path=DB_PATH, table_name=TABLE_NAME):
        self.db_path = db_path
        self.table_name = table_name
        self._ensure_db_dir_exists()

    def _ensure_db_dir_exists(self):
        """Asegura que el directorio de la base de datos exista."""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def connect(self):
        """Establece una conexión con la base de datos SQLite."""
        return sqlite3.connect(self.db_path)

    def create_table(self):
        """
        Crea la tabla 'averias_procesadas' si no existe.
        Define un esquema robusto para los datos limpios.
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Esquema de la tabla 'averias_procesadas'
        # Añadir 'id' autoincremental, y campos para datos limpios.
        # Considerar campos específicos que extraerás de 'Novedad'.
        # 'novedad_original' es útil para depuración.
        schema = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo TEXT NOT NULL,
            novedad_original TEXT,
            inicio_hora_falla DATETIME,
            fin_hora_falla DATETIME,
            horas_parada_minutos INTEGER, -- Calculado en ETL
            sistema_afectado TEXT,
            buque TEXT,
            --Campos adicionales extraídos de 'Novedad' o calculados
            tipo_averia_estandar TEXT,    -- Ej. "Falla Motor", "Mantenimiento Preventivo"
            componente_afectado TEXT,     -- Ej. "Bomba Hidráulica", "Cable de Carga"
            codigo_falla TEXT,            -- Si se extrae un código (ej. "E-205")
            fecha_procesamiento DATETIME DEFAULT CURRENT_TIMESTAMP,
            nombre_archivo_origen TEXT    -- Para trazabilidad
        );
        """
        cursor.execute(schema)
        conn.commit()
        conn.close()
        print(f"Tabla '{self.table_name}' asegurada en {self.db_path}")

    def insert_data(self, dataframe: pd.DataFrame, filename: str):
        """
        Inserta un DataFrame de Pandas en la tabla de la base de datos.
        Añade el nombre del archivo de origen.
        """
        conn = self.connect()
        try:
            # Asegurarse de que el nombre del archivo se añade antes de la inserción
            if 'nombre_archivo_origen' not in dataframe.columns:
                dataframe['nombre_archivo_origen'] = filename
            
            # Asegurarse de que las columnas del DataFrame coincidan con la tabla de DB.
            # Convertir nombres de columnas de snake_case para compatibilidad con SQL
            # (Pandas to_sql a menudo maneja esto, pero es buena práctica)
            df_for_db = dataframe.rename(columns={
                'Equipo': 'equipo',
                'Novedad': 'novedad_original', # Guarda el texto original
                'Inicio Hora Falla': 'inicio_hora_falla',
                'Hora Fin Falla': 'fin_hora_falla',
                'Sistema Afectado': 'sistema_afectado',
                'Buque': 'buque',
                'horas_parada_minutos': 'horas_parada_minutos',
                'tipo_averia_estandar': 'tipo_averia_estandar',
                'componente_afectado': 'componente_afectado',
                'codigo_falla': 'codigo_falla'
            })
            
            # Asegurarse de que solo las columnas que existen en la DB se inserten
            db_columns = self._get_table_columns()
            df_for_db = df_for_db[[col for col in db_columns if col in df_for_db.columns]]
            
            # Usar 'append' para añadir nuevos registros. Power BI puede manejar duplicados
            # o se puede añadir lógica aquí para evitar duplicados basada en una clave.
            df_for_db.to_sql(self.table_name, conn, if_exists='append', index=False)
            conn.commit()
            print(f"Datos del archivo '{filename}' insertados en '{self.table_name}'.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
            conn.rollback()
        finally:
            conn.close()

    def _get_table_columns(self):
        """Obtiene los nombres de las columnas de la tabla de la base de datos."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.table_name});")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        return columns

    def get_processed_files(self):
        """
        Recupera los nombres de archivos que ya han sido procesados
        (asumiendo que están almacenados en la columna 'nombre_archivo_origen').
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT nombre_archivo_origen FROM {self.table_name};")
        files = {row[0] for row in cursor.fetchall()}
        conn.close()
        return files