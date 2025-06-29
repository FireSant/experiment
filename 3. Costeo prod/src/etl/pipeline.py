import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data(data_path='data/'):
    """Extrae datos de los archivos CSV."""
    try:
        logging.info("Iniciando extracción de datos...")
        consumo_mat = pd.read_csv(f"{data_path}consumo_materiales.csv")
        costos_mat = pd.read_csv(f"{data_path}costos_materiales.csv")
        tiempos_mo = pd.read_csv(f"{data_path}tiempos_operador.csv")
        costos_mo = pd.read_csv(f"{data_path}costos_mo.csv")
        logging.info("Extracción completada.")
        return consumo_mat, costos_mat, tiempos_mo, costos_mo
    except FileNotFoundError as e:
        logging.error(f"Error: Archivo no encontrado - {e}")
        return None

def transform_data(consumo_mat, costos_mat, tiempos_mo, costos_mo):
    """Transforma y calcula los costos de los productos."""
    if consumo_mat is None:
        return None
    
    logging.info("Iniciando transformación de datos...")
    
    # 1. Calcular costo de materiales por producto
    costo_materiales_total = pd.merge(consumo_mat, costos_mat, on='id_material')
    costo_materiales_total['costo_total_material'] = costo_materiales_total['cantidad_usada'] * costo_materiales_total['costo_por_unidad']
    costo_materiales_por_producto = costo_materiales_total.groupby('id_producto')['costo_total_material'].sum().reset_index()

    # 2. Calcular costo de mano de obra por producto
    costo_mo_total = pd.merge(tiempos_mo, costos_mo, on='id_departamento')
    costo_mo_total['costo_total_mo'] = costo_mo_total['horas_hombre'] * costo_mo_total['costo_por_hora_hombre']
    costo_mo_por_producto = costo_mo_total.groupby('id_producto')['costo_total_mo'].sum().reset_index()

    # 3. Unir costos y calcular costo total
    df_final = pd.merge(costo_materiales_por_producto, costo_mo_por_producto, on='id_producto')
    
    # Asumimos un CIF (Costo Indirecto de Fabricación) del 20% del costo de mano de obra
    df_final['costo_cif'] = df_final['costo_total_mo'] * 0.20
    
    df_final['costo_total_producto'] = df_final['costo_total_material'] + df_final['costo_total_mo'] + df_final['costo_cif']
    
    logging.info("Transformación completada.")
    return df_final

def load_data(df, engine, output_csv_path=None):
    """Carga el DataFrame final a la base de datos PostgreSQL."""
    if df is None:
        logging.error("No hay datos para cargar.")
        return
    
    try:
        logging.info("Iniciando carga de datos a PostgreSQL...")
        df.to_sql('costos_productos_final', engine, if_exists='replace', index=False)
        logging.info("Carga completada exitosamente.")
    except Exception as e:
        logging.error(f"Error durante la carga a PostgreSQL: {e}")

    if output_csv_path:
        try:
            # --- CREAR DIRECTORIO SI NO EXISTE ---
            output_dir = os.path.dirname(output_csv_path)
            if output_dir and not os.path.exists(output_dir):
                logging.info(f"Creando directorio de salida: {output_dir}")
                os.makedirs(output_dir) # os.makedirs() crea directorios recursivamente
            # --- FIN DE CREAR DIRECTORIO ---

            logging.info(f"Iniciando carga de datos a CSV: {output_csv_path}...")
            df.to_csv(output_csv_path, index=False, encoding='utf-8')
            logging.info(f"Carga a CSV completada exitosamente en: {output_csv_path}")
        except Exception as e:
            logging.error(f"Error durante la carga a CSV: {e}")