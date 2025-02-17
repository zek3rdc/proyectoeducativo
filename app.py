import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestor",
    page_icon=":gear:",
    layout="wide",
    initial_sidebar_state="auto"
)

import os
import platform
from dependencias.security.config_manager import ConfigManager
from dependencias.security.logger import AppLogger
import bcrypt
import streamlit_authenticator as stauth
from modulos.dashboard import dashboard
from modulos.Utilidades.FuncionesGenerales import UI

# Inicializa la configuración y el logger
config_path = os.path.join(os.getcwd(), "config.yaml")
config_manager = ConfigManager(config_path)
logger = AppLogger()

# Asegurarse de que las contraseñas estén hasheadas
config_manager.update_passwords()

def checkSO():
    return platform.system()

def main():
    so = checkSO()
    logger.info(f"Gestoría se está ejecutando en sistema operativo {so}")

    ruta = "C:/Proyectos/UENB" if so == "Windows" else "/Proyectos/UENB"
    st.session_state['imgLogoPath'] = ruta + config_manager.get("imgLogoPath")
    st.session_state['imgIconPath'] = ruta + config_manager.get("imgIconPath")

    UI()

    # Configuración de autenticación
    authenticator = stauth.Authenticate(
        config_manager.get("credentials"),
        config_manager.get("cookie.name"),
        config_manager.get("cookie.key"),
        config_manager.get("cookie.expiry_days"),
    )
    
    authentication_status = authenticator.login(
        fields={'Form name': 'Iniciar Sesión', 'Username': 'Usuario', 'Password': 'Contraseña', 'Login': 'Acceder'}
    )

    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = authentication_status

    if st.session_state['authentication_status']:
        username = st.session_state['username']
        name = st.session_state['name']
        hashed_password = config_manager.get(f"credentials.usernames.{username}.password")
        user_role = config_manager.get(f"credentials.usernames.{username}.role")
        st.session_state['role'] = user_role
        user_permissions = config_manager.get(f"roles.{user_role}", [])
    

        # Agregar ID de acceso al session_state
        id_acceso = config_manager.get(f"credentials.usernames.{username}.id_acceso")
        st.session_state['id_acceso'] = id_acceso  # Asegurarse de que esté disponible para otros módulos
        id_acceso_admin = config_manager.get(f"credentials.usernames.{username}.acceso_calificaciones")
        st.session_state['acceso_calificaciones'] = id_acceso_admin  # Asegurarse de que esté disponible para otros módulos
        id_cordinates = config_manager.get(f"credentials.usernames.{username}.coordinate")
        st.session_state['coordinate'] = id_cordinates.lower() == "true" if isinstance(id_cordinates, str) else bool(id_cordinates)
        plantilla_path = config_manager.get("plantilla_path")
        st.session_state['plantilla_path']= plantilla_path
        output_path = config_manager.get("output_path")
        st.session_state['output_path']= output_path


        # Log de inicio de sesión
        logger.info(f"Usuario {username} inició sesión con rol {user_role} y ID de acceso {id_acceso}")

        st.sidebar.success(f"Bienvenido, {name}!")
        dashboard.app(user_permissions)

        if authenticator.logout("Cerrar Sesión", "sidebar"):
            st.cache_data.clear()
            logger.info(f"Usuario {username} cerró sesión.")
            st.success("Has cerrado sesión correctamente. La caché ha sido limpiada.")

    elif st.session_state['authentication_status'] is None:
        logger.warning("Intento de inicio de sesión fallido.")
        st.warning('Por favor introduzca su usuario y contraseña')

if __name__ == "__main__":
    main()
