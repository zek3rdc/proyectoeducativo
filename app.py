import streamlit as st
import warnings  # Importa warnings para manejar advertencias.
import os 
from yaml.loader import SafeLoader
import platform
import yaml
from modulos.Utilidades.FuncionesGenerales import UI
import streamlit_authenticator as stauth
from modulos.dashboard import dashboard 


# Cargar configuración desde un archivo YAML.
with open(os.getcwd() + '/config.yaml') as file: 
    config = yaml.load(file, Loader=SafeLoader) 


def checkSO():
    so = platform.system()
    return so

def main():
    # Obtiene la ruta del usuario actual.
    so= checkSO()
    print(f"Gestoria se esta ejecutando en sistema operativo {so}")
    ruta = ""
    if so=="Windows":
        ruta = "C:/Proyectos/UENB" 
    else:
        ruta = "/Proyectos/UENB" 

    st.session_state['imgLogoPath'] = ruta + config['imgLogoPath']
    st.session_state['imgIconPath'] = ruta + config['imgIconPath']

    # Configuración inicial de la página de Streamlit.
    st.set_page_config(
        page_title="Gestor",  # Título de la página.
        page_icon=st.session_state['imgIconPath'],  # Icono de la página.
        layout="wide",  # Diseño de la página.
        initial_sidebar_state="auto"  # Estado inicial de la barra lateral.
    )

    # CSS para hacer más brillante el logo, el muñeco y el texto "running"
    custom_css = """
    <style>
        /* Cambiar el color del logo */
        [data-testid="stHeader"] img {
            filter: brightness(5100%) saturate(1000%) invert(86%) sepia(602%) saturate(4604%) hue-rotate(57deg) brightness(102%) contrast(98%);
        }

        /* Hacer más brillante y notorio el muñeco animado de "running" */
        [data-testid="stStatusWidget"] svg {
            stroke: #c8f464 !important; /* Cambia el color del borde */
            fill: #c8f464 !important; /* Cambia el color interno */
            stroke-width: 2px; /* Aumenta el grosor del borde */
            filter: drop-shadow(0px 0px 6px #c8f464); /* Añade un resplandor */
        }

        /* Cambiar el color del texto 'running' */
        [data-testid="stStatusWidget"] {
            color: #c8f464 !important; /* Cambia el color del texto */
        }
    </style>
    """

    # Insertar el CSS en la aplicación
    st.markdown(custom_css, unsafe_allow_html=True)

    UI()
    

    # Configura la autenticación de usuarios.
    authenticator = stauth.Authenticate(
        config['credentials'],  # Credenciales de usuario.
        config['cookie']['name'],  # Nombre de la cookie.
        config['cookie']['key'],  # Clave de la cookie.
        config['cookie']['expiry_days'],  # Días de expiración de la cookie.
       
    )
    
    # Realiza el proceso de login.
    authentication_status= authenticator.login(fields={'Form name':'Iniciar Sesión','Username': 'Usuario', 'Password': 'Contraseña','Login':'Acceder'})

    # Almacena el estado de autenticación en st.session_state.
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = authentication_status

    # Si la autenticación es exitosa, muestra el dashboard.
    if st.session_state['authentication_status']:
        
        st.session_state['pass'] = True
        

        dashboard.app()  # Muestra el Dashboard de la aplicación.



        # Añade un botón de logout en la barra lateral.
        if authenticator.logout("Cerrar Sesión", "sidebar"):
    # Limpiar la caché de la aplicación
            st.cache_data.clear()  # Limpia la caché de datos de Streamlit

    # Opcional: Redirecciona a la página de inicio o muestra un mensaje de confirmación
            st.success("Has cerrado sesión correctamente. La caché ha sido limpiada.")


    # Si la autenticación está en proceso, muestra un mensaje de advertencia.
    elif st.session_state['authentication_status'] is None:
        st.warning('Por favor introduzca su usuario y contraseña')

# Ejecuta la aplicación principal si el script se ejecuta directamente.
if __name__ == "__main__":
    main()

# CSS para hacer más brillante el logo, el muñeco y el texto "running"
    custom_css = """
    <style>
        /* Cambiar el color del logo */
        [data-testid="stHeader"] img {
            filter: brightness(5100%) saturate(1000%) invert(86%) sepia(602%) saturate(4604%) hue-rotate(57deg) brightness(102%) contrast(98%);
        }

        /* Hacer más brillante y notorio el muñeco animado de "running" */
        [data-testid="stStatusWidget"] svg {
            stroke: #c8f464 !important; /* Cambia el color del borde */
            fill: #c8f464 !important; /* Cambia el color interno */
            stroke-width: 2px; /* Aumenta el grosor del borde */
            filter: drop-shadow(0px 0px 6px #c8f464); /* Añade un resplandor */
        }

        /* Cambiar el color del texto 'running' */
        [data-testid="stStatusWidget"] {
            color: #c8f464 !important; /* Cambia el color del texto */
        }
    </style>
    """

    # Insertar el CSS en la aplicación
    st.markdown(custom_css, unsafe_allow_html=True)