import streamlit as st
import pandas as pd
import sqlite3
import os

# 1. Obtiene la ruta absoluta de la carpeta donde está este script (DataVis.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Definimos las rutas completas a los archivos
db_path = os.path.join(BASE_DIR, 'logistica.db')
csv_path = os.path.join(BASE_DIR, 'plan_de_rutas.csv')

# --- Paleta de colores para las rutas ---
COLOR_PALETTE = [
    '#FF4B4B',  # Rojo
    '#4B7BFF',  # Azul
    '#4BFF7B',  # Verde
    '#E6A23C',  # Naranja
]

# Cargar datos de la base de datos
@st.cache_data
def load_data(ruta_db, ruta_csv):
    # Verificamos si la base de datos existe
    if not os.path.exists(ruta_db):
        raise FileNotFoundError(f"No se encontró la base de datos en: {ruta_db}")
    
    # Conexión a SQLite
    with sqlite3.connect(ruta_db) as conn:
        pedidos = pd.read_sql_query("SELECT * FROM pedidos", conn)
    
    # Intentar cargar el plan de rutas CSV
    try:
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError
        
        plan_rutas = pd.read_csv(ruta_csv)
        # Unimos los datos del DB con el CSV
        pedidos = pd.merge(pedidos, plan_rutas, on='id_pedido')
    except FileNotFoundError:
        # Si no hay plan, creamos la columna vacía y avisamos
        pedidos['ruta_asignada'] = None
        st.warning("No se encontró 'plan_de_rutas.csv'. Ejecuta primero el script de optimización.")
    
    return pedidos

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.title("Dashboard de Planificación Logística")

# Llamamos a la función usando las rutas calculadas arriba
df = load_data(db_path, csv_path)

st.subheader("Mapa de Entregas y Rutas Asignadas")

# Verificamos si hay rutas para colorear el mapa
if 'ruta_asignada' in df.columns and df['ruta_asignada'].notna().any():
    # Mapeo de colores según la ruta
    df['color'] = df['ruta_asignada'].apply(lambda x: COLOR_PALETTE[int(x) % len(COLOR_PALETTE)])
    st.map(df, latitude='latitud', longitude='longitud', color='color')
else:
    # Mapa simple si no hay rutas
    st.map(df, latitude='latitud', longitude='longitud')

st.subheader("Datos de Pedidos")
st.dataframe(df)

# Gráficos estadísticos si existen rutas
if 'ruta_asignada' in df.columns and df['ruta_asignada'].notna().any():
    st.subheader("Análisis de Carga por Ruta")
    
    # Agrupamos datos por ruta
    carga_por_ruta = df.groupby('ruta_asignada')[['peso_kg', 'volumen_m3']].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Peso (kg) por Ruta**")
        st.bar_chart(carga_por_ruta, x='ruta_asignada', y='peso_kg')
    
    with col2:
        st.write("**Volumen (m³) por Ruta**")
        st.bar_chart(carga_por_ruta, x='ruta_asignada', y='volumen_m3')