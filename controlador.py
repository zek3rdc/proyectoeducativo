import streamlit as st

def inicializar_estado(session_key="estado_inicial"):
    """Inicializa el estado de la sesión si no está previamente configurado."""
    if session_key not in st.session_state:
        st.session_state[session_key] = True

def evitar_recarga(session_key="estado_inicial"):
    """Evita que la página se recargue innecesariamente utilizando el estado de la sesión."""
    # Inicializamos la clave si no existe
    if session_key not in st.session_state:
        st.session_state[session_key] = True  # Primer cargado de la página

    # Verificar si es la primera carga de la página
    if st.session_state[session_key]:
        st.session_state[session_key] = False  # Indicamos que la página ya fue cargada
        return True  # La página se cargó por primera vez, se puede continuar
    return False  # La página ya ha sido recargada, no se hace nada adicional

def manejar_formulario(form_name, session_key="form_submitted"):
    """Gestiona la lógica de los formularios y evita su recarga innecesaria."""
    
    if form_name not in st.session_state:
        st.session_state[form_name] = False  # Indicamos que el formulario aún no ha sido enviado

    # Creamos el formulario
    with st.form(key=form_name):
        # Agrega tus campos de formulario aquí (por ejemplo, nombre, cédula, etc.)
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        cédula = st.text_input("Cédula")

        # Botón de envío
        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            st.session_state[form_name] = True  # Indicamos que el formulario fue enviado
            return True  # El formulario fue enviado correctamente

    return False  # Si el formulario no fue enviado, no hacemos nada adicional

def restablecer_estado_formulario(form_name):
    """Restablece el estado del formulario cuando sea necesario."""
    if form_name in st.session_state:
        st.session_state[form_name] = False  # Restablecemos el estado de envío del formulario

def restablecer_estado_general(session_key="estado_inicial"):
    """Restablece el estado general de la página, útil cuando se desea reiniciar la página."""
    if session_key in st.session_state:
        st.session_state[session_key] = True  # Marcamos que la página está lista para la próxima carga
