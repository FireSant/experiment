import boto3
import json
import time
import random
from datetime import datetime

# --- Configuración ---
S3_BUCKET_NAME = 'raw-sensor-data-bananabags'
ID_SENSORS = ['TEMP-01', 'TEMP-02', 'PRES-01', 'VIBR-01']
BATCH_SIZE = 20 # Número de lecturas a agrupar antes de subir
SECONDS_BETWEEN_READINGS = 2
SECONDS_BETWEEN_UPLOADS = BATCH_SIZE * SECONDS_BETWEEN_READINGS

# Inicializar cliente de S3
s3_client = boto3.client('s3')

def generate_sensor_reading(id_sensor):
    """Genera una lectura de sensor simulada."""
    value = 0
    if "TEMP" in id_sensor:
        # Simular una anomalía de temperatura ocasionalmente
        value = random.uniform(20.0, 95.0) if random.random() > 0.05 else random.uniform(95.1, 120.0)
        unit = 'C'
    elif "PRES" in id_sensor:
        value = random.uniform(1000.0, 1050.0)
        unit = 'hPa'
    elif "VIBR" in id_sensor:
        value = random.uniform(0.0, 5.0)
        unit = 'g'
        
    return {
        'id_sensor': id_sensor,
        'timestamp': datetime.now().isoformat(),
        'value': round(value, 2),
        'unit': unit
    }

def upload_to_s3(data, bucket, key):
    """Sube datos a un bucket de S3."""
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        print(f"Subido exitosamente el archivo {key} a {bucket}")
    except Exception as e:
        print(f"Error al subir a S3: {e}")

if __name__ == "__main__":
    readings_batch = []
    while True:
        for id_sensor in ID_SENSORS:
            reading = generate_sensor_reading(id_sensor)
            readings_batch.append(reading)
            print(f"Generado: {reading}")
            
            if len(readings_batch) >= BATCH_SIZE:
                # Crear un nombre de archivo único
                file_name = f"readings_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                upload_to_s3(readings_batch, S3_BUCKET_NAME, file_name)
                readings_batch = [] # Limpiar el lote
                print(f"Esperando {SECONDS_BETWEEN_UPLOADS} segundos para el próximo lote...")
                time.sleep(SECONDS_BETWEEN_UPLOADS)
            
            time.sleep(SECONDS_BETWEEN_READINGS)