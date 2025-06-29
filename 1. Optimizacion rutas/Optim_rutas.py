import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


db_path='logistica.db'


def optimizar_rutas(db_path, num_vehiculos):
    try:
        logging.info("Cargando datos de pedidos desde la base de datos...")
        with sqlite3.connect(db_path) as conn:
            pedidos_df = pd.read_sql_query("SELECT * FROM pedidos", conn)

        if pedidos_df.empty:
            logging.warning("No hay pedidos para optimizar.")
            return

        # --- Aplicación de Machine Learning (Clustering) ---
        logging.info(f"Aplicando K-Means para agrupar entregas en {num_vehiculos} clusters/rutas...")
        coordenadas = pedidos_df[['latitud', 'longitud']]
        kmeans = KMeans(n_clusters=num_vehiculos, random_state=42, n_init=10)
        pedidos_df['ruta_asignada'] = kmeans.fit_predict(coordenadas)

        # --- Lógica de Planificación (Simplificada) ---
        # Aquí iría un algoritmo de ruteo (TSP/VRP) para cada cluster.
        # Por simplicidad, por ahora solo guardaremos los clusters.
        # En un proyecto real, usarías librerías como OR-Tools de Google.
        logging.info("Agrupación de rutas completada.")

        # Guardar el plan de rutas
        plan_de_rutas = pedidos_df[['id_pedido', 'direccion_entrega', 'ruta_asignada']]
        plan_de_rutas.to_csv('plan_de_rutas.csv', index=False)
        logging.info("Plan de rutas guardado en 'plan_de_rutas.csv'")

    except Exception as e:
        logging.error(f"Ocurrió un error durante la optimización: {e}")

if __name__ == '__main__':
    # Suponemos que tenemos 4 vehículos disponibles
    optimizar_rutas('logistica.db', num_vehiculos=4)