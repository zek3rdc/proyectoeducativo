import streamlit as st
import warnings
import os 
from yaml.loader import SafeLoader
import platform
import yaml
from modulos.Utilidades.FuncionesGenerales import UI
import streamlit_authenticator as stauth
from modulos.dashboard import dashboard 

# Configuración inicial de la página de Streamlit
st.set_page_config(
    page_title="Gestor",
    page_icon=":gear:",
    layout="wide",
    initial_sidebar_state="auto"
)

# Cargar configuración desde el archivo YAML
with open(os.getcwd() + '/config.yaml') as file: 
    config = yaml.load(file, Loader=SafeLoader) 

def checkSO():
    return platform.system()

def get_user_role(username):
    return config['credentials']['usernames'][username]['role']

def get_role_permissions(role):
    return config['roles'].get(role, [])

def main():
    so = checkSO()
    print(f"Gestoria se está ejecutando en sistema operativo {so}")
    ruta = "C:/Proyectos/UENB" if so == "Windows" else "/Proyectos/UENB"

    st.session_state['imgLogoPath'] = ruta + config['imgLogoPath']
    st.session_state['imgIconPath'] = ruta + config['imgIconPath']

    # CSS personalizado (sin cambios)
    custom_css = """
    <style>
        [data-testid="stHeader"] img {
            filter: brightness(5100%) saturate(1000%) invert(86%) sepia(602%) saturate(4604%) hue-rotate(57deg) brightness(102%) contrast(98%);
        }
        [data-testid="stStatusWidget"] svg {
            stroke: #c8f464 !important;
            fill: #c8f464 !important;
            stroke-width: 2px;
            filter: drop-shadow(0px 0px 6px #c8f464);
        }
        [data-testid="stStatusWidget"] {
            color: #c8f464 !important;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    UI()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    
    authentication_status = authenticator.login(fields={'Form name':'Iniciar Sesión','Username': 'Usuario', 'Password': 'Contraseña','Login':'Acceder'})

    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = authentication_status

    if st.session_state['authentication_status']:
        st.session_state['pass'] = True
        username = st.session_state['username']
        name = st.session_state['name']
        user_role = get_user_role(username)
        user_permissions = get_role_permissions(user_role)

        # Mensaje de bienvenida en la barra lateral
        st.sidebar.success(f"Bienvenido, {name}!")

        # Pasar los permisos del usuario al dashboard
        dashboard.app(user_permissions)

        if authenticator.logout("Cerrar Sesión", "sidebar"):
            st.cache_data.clear()
            st.success("Has cerrado sesión correctamente. La caché ha sido limpiada.")

    elif st.session_state['authentication_status'] is None:
        st.warning('Por favor introduzca su usuario y contraseña')

if __name__ == "__main__":

    main()
