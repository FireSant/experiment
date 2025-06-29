import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pedidos_path="pedidos_diarios.csv"
vehiculos_path="vehiculos.csv"
def run_etl(pedidos_path, vehiculos_path, db_path):
    try:
        # EXTRACT
        logging.info("Extrayendo datos de los CSV...")
        pedidos_df = pd.read_csv(pedidos_path)
        vehiculos_df = pd.read_csv(vehiculos_path)

        # TRANSFORM
        logging.info("Transformando datos...")
        pedidos_df['fecha_pedido'] = pd.to_datetime(pedidos_df['fecha_pedido'])
        # Añadir validaciones: pesos/volúmenes no negativos, etc.
        pedidos_df = pedidos_df.dropna() # Simple manejo de nulos

        # LOAD
        logging.info(f"Cargando datos a la base de datos SQLite: {db_path}")
        with sqlite3.connect(db_path) as conn:
            pedidos_df.to_sql('pedidos', conn, if_exists='replace', index=False)
            vehiculos_df.to_sql('vehiculos', conn, if_exists='replace', index=False)
        logging.info("ETL completado exitosamente.")

    except Exception as e:
        logging.error(f"Ocurrió un error en el proceso ETL: {e}")

if __name__ == '__main__':
    run_etl('pedidos_diarios.csv', 'vehiculos.csv', 'logistica.db')