import streamlit as st
import pandas as pd
import sqlite3
import os

# Ruta a la base de datos  
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'logistica.db')

# --- Definimos una paleta de colores ---
# Puedes añadir más colores si tienes más de 3 rutas/vehículos
COLOR_PALETTE = [
    '#FF4B4B',  # Rojo
    '#4B7BFF',  # Azul
    '#4BFF7B',  # Verde
    '#E6A23C',  # Naranja
]

# Cargar datos de la base de datos
@st.cache_data
def load_data(db_path):
    with sqlite3.connect(db_path) as conn:
        pedidos = pd.read_sql_query("SELECT * FROM pedidos", conn)
    try:
        # Cargar el plan de rutas si existe
        plan_rutas = pd.read_csv('plan_de_rutas.csv')
        pedidos = pd.merge(pedidos, plan_rutas, on='id_pedido')
    except FileNotFoundError:
        # Si no hay plan, creamos una columna vacía para evitar errores
        pedidos['ruta_asignada'] = None
        st.warning("Ejecuta primero el script de optimización para ver las rutas.")
    return pedidos

st.title("Dashboard de Planificación Logística")

df = load_data('logistica.db')

st.subheader("Mapa de Entregas y Rutas Asignadas")

if 'ruta_asignada' in df.columns and df['ruta_asignada'].notna().any():
    # Creamos una nueva columna 'color' mapeando el número de ruta a un color de nuestra paleta
    # Usamos el operador módulo (%) para que si hay más rutas que colores, los colores se repitan
    df['color'] = df['ruta_asignada'].apply(lambda x: COLOR_PALETTE[int(x) % len(COLOR_PALETTE)])
    
    # Ahora le pasamos la nueva columna 'color' al argumento color de st.map
    st.map(df, latitude='latitud', longitude='longitud', color='color')
else:
    # Si no hay rutas asignadas, mostramos el mapa sin colores
    st.map(df, latitude='latitud', longitude='longitud')


st.subheader("Datos de Pedidos")
st.dataframe(df)

# Añadir más gráficos: pedidos por día, peso total por ruta, etc.
if 'ruta_asignada' in df.columns and df['ruta_asignada'].notna().any():
    st.subheader("Carga por Ruta")
    carga_por_ruta = df.groupby('ruta_asignada')[['peso_kg', 'volumen_m3']].sum().reset_index()
    
    # Gráfico de barras para el peso
    st.write("Peso (kg) por Ruta")
    st.bar_chart(carga_por_ruta, x='ruta_asignada', y='peso_kg')
    
    # Gráfico de barras para el volumen
    st.write("Volumen (m³) por Ruta")
    st.bar_chart(carga_por_ruta, x='ruta_asignada', y='volumen_m3')