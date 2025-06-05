# app/main.py

import streamlit as st
import numpy as np
from PIL import Image
from markov.modelo import CadenasDeMarkovIA
import pandas as pd

# Configuración de la página (debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="NEXT-AI-KOV",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS para una apariencia moderna tipo Facebook
st.markdown("""
<style>
    body {
        background: #0F172A !important; /* Dark blue/slate background */
        color: #E2E8F0 !important; /* Light gray/slate text */
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .main {
        background: transparent !important;
    }
    .stApp {
        background: #0F172A !important; /* Dark blue/slate background */
        color: #E2E8F0 !important;
    }
    /* General Markdown text color */
    .stMarkdown {
        color: #E2E8F0 !important;
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        height: 56px;
        font-size: 18px;
        margin: 16px 0;
        border-radius: 12px;
        background-color: #3B82F6; /* Brighter blue for buttons on dark bg */
        color: #FFFFFF;
        border: none;
        box-shadow: 0 2px 8px rgba(59,130,246,0.15);
        transition: background 0.2s, box-shadow 0.2s;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #2563EB; /* Darker blue on hover */
        box-shadow: 0 4px 16px rgba(59,130,246,0.2);
    }
    /* Specific styles for sidebar buttons */
    .stSidebar .stButton > button {
        background-color: transparent;
        color: #E2E8F0; /* Light text for sidebar buttons */
        font-weight: 500;
        text-align: left;
        padding-left: 10px;
        margin: 8px 0;
        box-shadow: none;
    }
    .stSidebar .stButton > button:hover {
        background-color: #1E293B; /* Darker slate on hover for sidebar */
        color: #3B82F6; /* Blue accent on hover */
        box-shadow: none;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        width: 100%;
        font-size: 17px;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #334155; /* Slate border */
        background: #1E293B; /* Dark slate input background */
        color: #E2E8F0; /* Light text in inputs */
        margin-bottom: 12px;
    }
    .stTextInput > div > label,
    .stNumberInput > div > label {
        color: #94A3B8 !important; /* Lighter label color for inputs */
    }
    .stDataFrame {
        margin: 20px 0;
        padding: 20px;
        border-radius: 16px;
        background: #1E293B; /* Dark slate for dataframes */
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #334155;
    }
    /* Ensure table headers and cells are readable */
    .stDataFrame table th {
        background-color: #334155;
        color: #E2E8F0;
    }
    .stDataFrame table td {
        color: #CBD5E1;
    }
    .stSelectbox > div > div > div {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E2E8F0 !important;
    }
    .stSelectbox > label {
        color: #94A3B8 !important;
    }
    .card {
        background: #1E293B; /* Dark slate for cards */
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        padding: 32px 24px;
        margin-bottom: 32px;
        border: 1px solid #334155;
    }
    .facebook-title {
        color: #60A5FA; /* Light blue title */
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-top: 20px;
        margin-bottom: 5px;
        text-align: center;
        text-shadow: 0 1px 3px rgba(96,165,250,0.15);
    }
    .facebook-subtitle {
        color: #94A3B8; /* Lighter subtitle color */
        font-size: 1.1rem;
        font-weight: 400;
        text-align: center;
        margin-bottom: 30px;
    }
    .sidebar .sidebar-content {
        background: #1E293B !important; /* Dark slate sidebar background */
        border-radius: 0px;
        border-right: 1px solid #334155; /* Slate border */
        padding: 15px;
    }
    .stSidebar .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5); /* Focus ring */
    }
    /* Ensure Streamlit's default success/info/warning/error boxes are styled for dark mode */
    .stAlert {
        background-color: #334155 !important;
        color: #E2E8F0 !important;
        border-color: #475569 !important;
    }
    .stAlert a {
        color: #60A5FA !important;
    }
    .responsive-logo img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 60%; /* Default scaling relative to container */
        max-width: 350px; /* Max width on larger screens */
        height: auto; /* Maintain aspect ratio */
    }
</style>
""", unsafe_allow_html=True)

# Función para mostrar el encabezado principal con logo
def mostrar_encabezado_principal():
    st.markdown("<div class='responsive-logo'>", unsafe_allow_html=True)
    try:
        # Usar ruta relativa compatible con cualquier SO
        import os
        logo_path = os.path.join("assets", "Logo.png")
        if not os.path.exists(logo_path):
            st.warning(f"⚠️ No se encontró el logo en: {os.path.abspath(logo_path)}")
        else:
            logo = Image.open(logo_path)
            st.image(logo, use_column_width=True)  # Se adapta al ancho de la columna
    except Exception as e:
        st.error(f"Error al cargar el logo: {str(e)}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='facebook-title'>NEXT-AI-KOV</h1>", unsafe_allow_html=True)
    st.markdown("<p class='facebook-subtitle'>Simulador de Navegación IA con Cadenas de Markov</p>", unsafe_allow_html=True)

# Mostrar el encabezado principal en todas las páginas
mostrar_encabezado_principal()

# Inicializar sesión
if 'modo' not in st.session_state:
    st.session_state['modo'] = None
    st.session_state['num_usuarios'] = 100
    st.session_state['num_usos'] = 20
    st.session_state['pagina_actual'] = "Inicio"

# Función para navegar
def navegar_a_pagina(pagina):
    st.session_state['pagina_actual'] = pagina
    st.rerun()

# Menú principal en la sidebar
st.sidebar.title("Navegación")
st.sidebar.markdown("---") # Visual separator

if st.sidebar.button("🚀  Inicio", key="btn_inicio"):
    navegar_a_pagina("Inicio")
if st.sidebar.button("📊  Análisis de Datos", key="btn_analisis"):
    navegar_a_pagina("Análisis de Datos")
if st.sidebar.button("🏆  Créditos", key="btn_creditos"):
    navegar_a_pagina("Créditos")
if st.sidebar.button("🚪  Salir", key="btn_salir"):
    navegar_a_pagina("Salir")
st.sidebar.markdown("---") # Visual separator

# Función para mostrar la página de inicio
def mostrar_inicio():
    # El título "NEXT-AI-KOV" ya no es necesario aquí, pues está en el encabezado global.
    # Sin embargo, podemos poner un subtítulo específico para la página de inicio si se desea.
    # st.subheader("Bienvenido al Simulador") # Ejemplo de subtítulo de página
    pass # El contenido principal de la página de inicio (botones, texto) sigue abajo.

    # Simplified buttons without columns
    if st.button("Iniciar Análisis Automático", key='auto_btn_inicio'):
        st.session_state['modo'] = 'automatico'
        st.session_state['num_usuarios'] = 100  # Default values
        st.session_state['num_usos'] = 20      # Default values
        navegar_a_pagina(" Análisis de Datos") # Note the leading space

    if st.button("Configurar Análisis Manual", key='manual_btn_inicio'):
        st.session_state['modo'] = 'manual'
        st.session_state['num_usuarios'] = 100  # Default values
        st.session_state['num_usos'] = 20      # Default values
        navegar_a_pagina(" Análisis de Datos") # Note the leading space
    
    # Mostrar texto después de los botones
    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <h2>Bienvenido a NEXT-AI-KOV</h2>
        <p style='font-size: 18px; margin: 20px 0;'>
            La solución más avanzada para el análisis de comportamiento de usuarios en plataformas de IA usando cadenas de Markov.
        </p>
        <p style='font-size: 16px;'>
            Con NEXT-AI-KOV puedes:
            <ul style='text-align: left; margin-left: 40px;'>
                <li>Simular el comportamiento de usuarios entre diferentes plataformas de IA</li>
                <li>Analizar patrones de navegación y transición</li>
                <li>Generar recomendaciones personalizadas</li>
                <li>Visualizar estadísticas y métricas en tiempo real</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

def mostrar_analisis_datos():
    if 'modo' not in st.session_state:
        st.warning("Por favor, selecciona un modo de análisis desde la página de inicio")
        return
    
    # Si estamos en modo manual, mostrar la configuración
    if st.session_state['modo'] == 'manual':
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Configuración Manual")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Configuración de Simulación")
            num_usuarios = st.number_input(
                "Número de usuarios (en millones)",
                min_value=1.0,
                max_value=500.0,
                value=100.0,
                step=1.0,
                help="Número de usuarios simulados en millones"
            )
            num_usos = st.number_input(
                "Número promedio de usos por usuario",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                help="Número promedio de interacciones por usuario"
            )
        with col2:
            if st.button("Iniciar Análisis"):
                st.session_state['num_usuarios'] = int(num_usuarios * 1000)
                st.session_state['num_usos'] = num_usos
                st.session_state['modo'] = 'automatico'
                st.rerun()  # Forzar actualización inmediata
        st.markdown('</div>', unsafe_allow_html=True)
        return  # Salir aquí para no mostrar la parte de resultados

    # Si estamos en modo automático, mostrar los resultados
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Análisis Automático")
    st.write("Datos obtenidos de Google Analytics (ID: GA-123456789)")
    # Crear y simular modelo
    modelo = CadenasDeMarkovIA(
        num_usuarios=st.session_state['num_usuarios'],
        num_usos=st.session_state['num_usos']
    )
    modelo.simular()
    # Mostrar matrices con etiquetas y explicaciones
    st.subheader("Estado Inicial")
    st.write("Este vector muestra la distribución inicial de los usuarios entre las plataformas.")
    st.dataframe(modelo.formatear_matriz(modelo.calcular_estado_inicial(), 'inicial'))
    st.subheader("Matriz de Transición")
    st.write("Esta matriz muestra las probabilidades de transición entre las diferentes plataformas de IA.")
    st.dataframe(modelo.formatear_matriz(modelo.calcular_matriz_transicion(), 'transicion'))
    st.subheader("Estado a Largo Plazo (Estado Estacionario)")
    st.write("Este vector muestra la distribución de usuarios a largo plazo (estado estacionario) entre las plataformas.")
    st.dataframe(modelo.formatear_matriz(modelo.calcular_estado_largo_plazo(), 'largo'))
    # Mostrar conclusión
    st.subheader("Análisis y Recomendaciones")
    conclusion = modelo.generar_conclusion()
    st.markdown("""
    <div style='text-align: justify; margin: 20px;'>
        <p style='font-size: 16px;'>""" + conclusion + """</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def mostrar_creditos():
    st.title("Créditos")
    
    info_html = """
    <div style='text-align: center; margin: 20px;'>
        <h2>Desarrollado por:</h2>
        <p style='font-size: 18px; margin: 10px 0;'>Jheanpiere Cerdan</p>
        <p style='font-size: 16px;'>
            <strong>Carrera:</strong> Ingeniería de Sistemas de la Información<br>
            <strong>Universidad:</strong> UPC<br>
            <strong>Curso:</strong> Matemáticas Discretas
        </p>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

    contact_html = """
    <div style='text-align: center; margin: 20px;'>
        <h3>Contacto:</h3>
        <p style="font-size: 16px; line-height: 1.5;">
            <strong>Email:</strong> <a href="mailto:U20241E898@UPC.EDU.PE">U20241E898@UPC.EDU.PE</a><br>
            <strong>GitHub:</strong> <a href="https://github.com/jacsontheguitars" target="_blank" rel="noopener noreferrer">@jacsontheguitars</a>
        </p>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)

def mostrar_salir():
    st.title("Salir")
    st.markdown("""
    <div style='text-align: center; margin: 20px;'>
        <p style='font-size: 18px;'>¿Estás seguro que deseas salir de la aplicación?</p>
        <button onclick="window.location.href='/'" style='padding: 10px 20px; font-size: 16px; border-radius: 5px; background-color: #dc3545; color: white; border: none; cursor: pointer;'>Sí, salir</button>
    </div>
    """, unsafe_allow_html=True)

# Mostrar la página correspondiente
if 'pagina_actual' not in st.session_state:
    st.session_state['pagina_actual'] = "Inicio"  # Default a Inicio si no existe

if st.session_state['pagina_actual'] == "Inicio":
    mostrar_inicio()
elif st.session_state['pagina_actual'] == "Análisis de Datos":
    mostrar_analisis_datos()
elif st.session_state['pagina_actual'] == "Créditos":
    mostrar_creditos()
elif st.session_state['pagina_actual'] == "Salir":
    mostrar_salir()

