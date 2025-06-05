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
        navegar_a_pagina("Análisis de Datos")  # Corregido: eliminado espacio al inicio

    if st.button("Configurar Análisis Manual", key='manual_btn_inicio'):
        st.session_state['modo'] = 'manual'
        st.session_state['num_usuarios'] = 100  # Default values
        st.session_state['num_usos'] = 20      # Default values
        navegar_a_pagina("Análisis de Datos")  # Corregido: eliminado espacio al inicio
