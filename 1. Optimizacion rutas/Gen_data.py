import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
NUM_PEDIDOS = 200
FECHA_INICIO = "2025-06-01"
DIAS_RANGO = 15
ARCHIVO_PEDIDOS = 'pedidos_diarios.csv'
ARCHIVO_VEHICULOS = 'vehiculos.csv'

# Inicializar Faker para español
fake = Faker('es_ES')

# --- UBICACIONES REALISTAS EN ECUADOR (Lat, Lon) ---
# Se incluyen barrios y ciudades para mayor granularidad
ubicaciones = {
    # Guayaquil y alrededores
    "Guayaquil - Centro": (-2.1962, -79.8822),
    "Guayaquil - Urdesa": (-2.1709, -79.9094),
    "Guayaquil - Samborondón": (-2.1450, -79.8678),
    "Durán": (-2.1733, -79.8256),
    "Daule": (-1.8639, -79.9786),
    
    # Quito y alrededores
    "Quito - La Mariscal": (-0.2092, -78.4918),
    "Quito - Centro Histórico": (-0.2202, -78.5119),
    "Quito - Cumbayá": (-0.2036, -78.4342),
    
    # Otras ciudades principales
    "Cuenca": (-2.9005, -79.0045),
    "Manta": (-0.9661, -80.7123),
    "Ambato": (-1.2490, -78.6168),
    "Machala": (-3.2581, -79.9605),
    "Santo Domingo": (-0.2389, -79.1774),
    "Portoviejo": (-1.0556, -80.4545),
    "Loja": (-3.9833, -79.2042),
    "Esmeraldas": (0.9676, -79.6546),
    "Ibarra": (0.3387, -78.1223),
    "Quevedo": (-1.0286, -79.4635),
    "Riobamba": (-1.6636, -78.6547),
    "Latacunga": (-0.9319, -78.6169)
}

# --- GENERACIÓN DE DATOS DE VEHÍCULOS ---
def generar_vehiculos():
    """Genera un DataFrame con datos de vehículos."""
    data_vehiculos = {
        'id_vehiculo': ['V-001', 'V-002', 'V-003', 'V-004'],
        'capacidad_max_kg': [1000, 1200, 800, 1500],
        'capacidad_max_m3': [6, 7, 5, 9],
        'costo_km': [0.50, 0.55, 0.45, 0.60]
    }
    return pd.DataFrame(data_vehiculos)

# --- GENERACIÓN DE DATOS DE PEDIDOS ---
def generar_pedidos(num_pedidos):
    """Genera un DataFrame con datos de pedidos simulados."""
    lista_pedidos = []
    fecha_inicio_dt = datetime.strptime(FECHA_INICIO, "%Y-%m-%d")

    for i in range(1, num_pedidos + 1):
        # Seleccionar una ubicación aleatoria
        nombre_ubicacion, (lat, lon) = random.choice(list(ubicaciones.items()))
        
        # Añadir una pequeña variación a las coordenadas para no tener puntos exactos
        lat_ruido = lat + np.random.normal(0, 0.01)
        lon_ruido = lon + np.random.normal(0, 0.01)

        # Generar fecha aleatoria
        dias_aleatorios = random.randint(0, DIAS_RANGO)
        fecha_aleatoria = fecha_inicio_dt + timedelta(days=dias_aleatorios)

        pedido = {
            'id_pedido': f'PED-{str(i).zfill(5)}',
            'id_cliente': f'CLI-{str(random.randint(1, 50)).zfill(3)}',
            'direccion_entrega': f"{fake.street_address()}, {nombre_ubicacion}",
            'latitud': round(lat_ruido, 6),
            'longitud': round(lon_ruido, 6),
            'peso_kg': round(random.uniform(1.0, 100.0), 2),
            'volumen_m3': round(random.uniform(0.01, 1.5), 3),
            'fecha_pedido': fecha_aleatoria.strftime("%Y-%m-%d %H:%M:%S")
        }
        lista_pedidos.append(pedido)
    
    return pd.DataFrame(lista_pedidos)

# --- FUNCIÓN PRINCIPAL ---
def main():
    """Función principal para generar y guardar los archivos CSV."""
    print("Generando datos de vehículos...")
    df_vehiculos = generar_vehiculos()
    df_vehiculos.to_csv(ARCHIVO_VEHICULOS, index=False)
    print(f"Archivo '{ARCHIVO_VEHICULOS}' generado con {len(df_vehiculos)} registros.")

    print("\nGenerando datos de pedidos...")
    df_pedidos = generar_pedidos(NUM_PEDIDOS)
    df_pedidos.to_csv(ARCHIVO_PEDIDOS, index=False)
    print(f"Archivo '{ARCHIVO_PEDIDOS}' generado con {len(df_pedidos)} registros.")
    
    print("\n¡Proceso completado!")

if __name__ == '__main__':
    main()