import traceback
import json
import boto3
import os
from datetime import datetime

# Inicializar clientes de AWS fuera del handler para reutilización
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

PROCESSED_BUCKET = os.environ['PROCESSED_BUCKET_NAME']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
TEMP_THRESHOLD = 85.0

def lambda_handler(event, context):
    print("LAMBDA INICIADA: Iniciando procesamiento del evento.") # NUEVO
    
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Procesando archivo: s3://{source_bucket}/{source_key}")
    
    try:
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        content = response['Body'].read().decode('utf-8')
        sensor_readings = json.loads(content)
        print("Datos leídos y parseados de S3.") # NUEVO
        
        for reading in sensor_readings:
            id_sensor = reading['id_sensor']
            timestamp = reading['timestamp']
            value = reading['value']
            
            # Almacenar el último estado en DynamoDB
            table = dynamodb.Table(DYNAMODB_TABLE)
            table.put_item(
                Item={
                    'id_sensor': id_sensor,
                    'last_value': str(value), 
                    'last_timestamp': timestamp,
                    'unit': reading['unit']
                }
            )
            print(f"Dato de {id_sensor} escrito en DynamoDB.") # NUEVO
            
            # Comprobar si hay anomalías y enviar alerta
            if 'TEMP' in id_sensor and value > TEMP_THRESHOLD:
                message = (
                    f"¡ALERTA DE TEMPERATURA ALTA!\n\n"
                    f"ID Sensor: {id_sensor}\n"
                    f"Temperatura Detectada: {value}°C\n"
                    f"Umbral Superado: {TEMP_THRESHOLD}°C\n"
                    f"Timestamp: {timestamp}"
                )
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=message,
                    Subject=f"Alerta de Temperatura: {id_sensor}"
                )
                print(f"ALERTA DE SNS ENVIADA para {id_sensor}") # NUEVO

        # Guardar el archivo procesado en el bucket de "processed-data"
        processed_key = f"processed_{source_key}"
        s3_client.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=processed_key,
            Body=json.dumps(sensor_readings),
            ContentType='application/json'
        )
        print(f"Archivo {processed_key} escrito en S3 processed.") # NUEVO
        
        # (Opcional) Borrar el archivo original
        s3_client.delete_object(Bucket=source_bucket, Key=source_key)
        print(f"Archivo original {source_key} borrado de S3 raw.") # NUEVO

        return {
            'statusCode': 200,
            'body': json.dumps(f'Procesado exitosamente el archivo {source_key}')
        }
        
    except Exception as e:
        print(f"ERROR: Se capturó una excepción: {e}") # MEJORADO
        print(f"TRACEBACK: {traceback.format_exc()}") # NUEVO: Requiere 'import traceback' al inicio
        raise e # Es crucial volver a lanzar la excepción para que Lambda la registre como un fallo