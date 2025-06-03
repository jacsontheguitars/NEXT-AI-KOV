# app/main.py


import streamlit as st
import numpy as np
from markov.modelo import CadenasDeMarkov

st.set_page_config(page_title="Cadenas de Markov", layout="centered")

st.title("🔄 Simulación de Cadenas de Markov")
st.markdown("Simula el comportamiento de usuarios en plataformas digitales usando cadenas de Markov.")

# Entradas del usuario
num_usuarios = st.slider("Número de usuarios:", min_value=10, max_value=500, value=100, step=10)
num_usos = st.slider("Número de usos por usuario:", min_value=5, max_value=100, value=20, step=5)

# Botón para correr simulación
if st.button("Ejecutar simulación"):
    modelo = CadenasDeMarkov(num_usuarios=num_usuarios, num_usos=num_usos)
    modelo.simular()
    
    matriz = modelo.calcular_matriz_transicion()
    estado_inicial = modelo.calcular_estado_inicial()
    estado_largo_plazo = modelo.calcular_estado_largo_plazo(estado_inicial, matriz)
    plataformas = modelo.plataformas

    st.subheader("📊 Matriz de Transición")
    st.dataframe(np.round(matriz, 2), use_container_width=True)

    st.subheader("🚦 Estado Inicial")
    estado_inicial_dict = {plataformas[i]: round(p, 2) for i, p in enumerate(estado_inicial)}
    st.json(estado_inicial_dict)

    st.subheader("📈 Estado a Largo Plazo")
    estado_largo_dict = {plataformas[i]: round(p, 2) for i, p in enumerate(estado_largo_plazo)}
    st.json(estado_largo_dict)
