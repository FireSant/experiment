import pandas as pd
import random
from faker import Faker

# Inicializamos Faker para generar nombres aleatorios
fake = Faker()

# --- CONFIGURACIÓN ---
NUM_MATERIALES = 10
NUM_PRODUCTOS = 20
NUM_DEPARTAMENTOS = 5
NUM_CONSUMOS = 50
NUM_TIEMPOS = 50

# --- GENERADOR DE DATOS ---

def generar_costos_materiales():
    """Genera datos de costos de materiales."""
    materiales = [f"MAT-{str(i).zfill(3)}" for i in range(1, NUM_MATERIALES + 1)]
    nombres_materiales = [fake.word().capitalize() for _ in materiales]
    costos_por_unidad = [round(random.uniform(5, 50), 2) for _ in materiales]

    df = pd.DataFrame({
        "id_material": materiales,
        "nombre_material": nombres_materiales,
        "costo_por_unidad": costos_por_unidad
    })
    df.to_csv("data/costos_materiales.csv", index=False)
    print("Archivo 'costos_materiales.csv' generado.")

def generar_consumo_materiales():
    """Genera datos de consumo de materiales por producto."""
    productos = [f"PROD-{str(i).zfill(3)}" for i in range(1, NUM_PRODUCTOS + 1)]
    materiales = [f"MAT-{str(i).zfill(3)}" for i in range(1, NUM_MATERIALES + 1)]
    consumo = []

    for _ in range(NUM_CONSUMOS):
        producto = random.choice(productos)
        material = random.choice(materiales)
        cantidad_usada = round(random.uniform(1, 10), 2)
        consumo.append({"id_producto": producto, "id_material": material, "cantidad_usada": cantidad_usada})

    df = pd.DataFrame(consumo)
    df.to_csv("data/consumo_materiales.csv", index=False)
    print("Archivo 'consumo_materiales.csv' generado.")

def generar_costos_mo():
    """Genera datos de costos de mano de obra por departamento."""
    departamentos = [f"DEP-{str(i).zfill(3)}" for i in range(1, NUM_DEPARTAMENTOS + 1)]
    costos_por_hora = [round(random.uniform(10, 25), 2) for _ in departamentos]

    df = pd.DataFrame({
        "id_departamento": departamentos,
        "costo_por_hora_hombre": costos_por_hora
    })
    df.to_csv("data/costos_mo.csv", index=False)
    print("Archivo 'costos_mo.csv' generado.")

def generar_tiempos_operador():
    """Genera datos de tiempos de operador por producto y departamento."""
    productos = [f"PROD-{str(i).zfill(3)}" for i in range(1, NUM_PRODUCTOS + 1)]
    departamentos = [f"DEP-{str(i).zfill(3)}" for i in range(1, NUM_DEPARTAMENTOS + 1)]
    tiempos = []

    for _ in range(NUM_TIEMPOS):
        producto = random.choice(productos)
        departamento = random.choice(departamentos)
        horas_hombre = round(random.uniform(1, 5), 2)
        tiempos.append({"id_producto": producto, "id_departamento": departamento, "horas_hombre": horas_hombre})

    df = pd.DataFrame(tiempos)
    df.to_csv("data/tiempos_operador.csv", index=False)
    print("Archivo 'tiempos_operador.csv' generado.")

# --- FUNCIÓN PRINCIPAL ---
def main():
    """Genera todos los datos necesarios para el proyecto."""
    print("Generando datos simulados...")
    generar_costos_materiales()
    generar_consumo_materiales()
    generar_costos_mo()
    generar_tiempos_operador()
    print("¡Todos los archivos han sido generados exitosamente!")

if __name__ == "__main__":
    main()