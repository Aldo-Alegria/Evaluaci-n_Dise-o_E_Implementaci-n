import os
import sys
import subprocess
import time
import webbrowser # Nueva importación para forzar la apertura

# ==========================================================
# 1. FUNCIÓN DE AUTO-LANZAMIENTO MEJORADA
# ==========================================================
def iniciar_interfaz():
    if "streamlit" not in sys.modules:
        # Definimos el puerto (estilo Flask)
        puerto = os.environ.get("PORT", "8501")
        url = f"http://localhost:{puerto}"
        
        print(f"--- Iniciando Servidor en {url} ---")
        
        # Forzamos la apertura del navegador después de un pequeño delay
        # para dar tiempo a que el servidor levante
        webbrowser.open(url)
        
        # Ejecutamos Streamlit como un módulo de Python
        comando = [
            sys.executable, "-m", "streamlit", "run", sys.argv[0], 
            "--server.port", str(puerto), 
            "--server.address", "0.0.0.0",
            "--server.headless", "true" # Evita conflictos de apertura doble
        ]
        
        try:
            subprocess.run(comando)
        except Exception as e:
            print(f"Error crítico al lanzar: {e}")
        sys.exit()

# Ejecutar el lanzador antes de cualquier otra cosa
iniciar_interfaz()

# ==========================================================
# 2. CÓDIGO DE LA APLICACIÓN (Bajo Streamlit)
# ==========================================================
import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPD - Eventos", layout="wide")
st.title("Participación de Deportistas Peruanos en Eventos Internacionales")

@st.cache_data
def cargar_datos():
    try:
        # Carga del archivo proporcionado con el separador detectado
        df = pd.read_csv('Data_DeportistasEventos_0.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
        return df
    except Exception as e:
        st.error(f"Archivo no encontrado o error de lectura: {e}")
        return None

df = cargar_datos()

if df is not None:
    st.success(f"Base de Datos cargada: {len(df):,} registros.")
    
    # Diferenciación técnica solicitada
    with st.sidebar:
        st.header("Arquitectura de Datos")
        st.write("**Centralizado:** Este script corre localmente procesando el CSV.")
        st.write("**Distribuido:** Integración futura con MongoDB Atlas para escalabilidad.")

    # Gráfico de actividad
    st.subheader("Top 10 Federaciones con mayor presencia internacional")
    st.bar_chart(df['FEDERACION'].value_counts().head(10))

    # Vista previa
    st.subheader("Detalle de Participaciones")
    st.dataframe(df.head(100), use_container_width=True)

# ==========================================================
# 3. BLOQUE DE EJECUCIÓN FINAL (Referencia Flask)
# ==========================================================
if __name__ == "__main__":
    # Si por alguna razón el primer check falla, este bloque asegura el inicio
    iniciar_interfaz()