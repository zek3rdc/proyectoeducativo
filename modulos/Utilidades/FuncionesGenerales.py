
import streamlit as st  # Importa la librería Streamlit para crear aplicaciones web.
from streamlit.components.v1 import html




def UI():
    
    
    with st.container():
        
      
        st.sidebar.image(st.session_state['imgLogoPath'])
        rainbow_css = """
        <style>
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }

        .rainbow-text {
            font-size: 28px; /* Ajusta el tamaño según sea necesario */
            font-weight: bold;
            background: linear-gradient(90deg, #FF5733, #FFBD33, #75FF33, #33FF57, #33FFBD, #3375FF, #5733FF, #FF33A1);
            background-size: 400%; /* Ajusta para una animación más suave */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: rainbow 6s linear infinite; /* Duración de la animación */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Sombra para un efecto más profesional */
            letter-spacing: 1px; /* Espaciado entre letras */
        }
        </style>
        """

        # Agregar el CSS a la aplicación
        st.markdown(rainbow_css, unsafe_allow_html=True)

        # Usar el texto con el efecto arcoíris
        st.sidebar.markdown('<div class="rainbow-text">v2025.02.01 ALPHA</div>', unsafe_allow_html=True)
                
    # Remove whitespace from the top of the page and sidebar
        st.markdown("""
                <style>
                    
                .st-emotion-cache-7818fn{
                    padding-top: 2rem;

                }    
                    
               .block-container {
                    padding-top: 0rem;
                } 
                    
                /*    
                [data-testid="element-container"] iframe {
                height: 0 !important; /* Mantener el iframe oculto */
                margin: 0 !important; /* Eliminar cualquier margen alrededor */
                padding: 0 !important; /* Eliminar cualquier padding adicional */
                display: block !important; /* Asegura que el iframe no afecte al layout */
                }
                */
                [data-testid="element-container"] {
                    margin: 0 !important; /* Eliminar márgenes del div */
                    padding: 0 !important; /* Eliminar padding del div */
                }
                                
             
                </style>
                    """, unsafe_allow_html=True)


        html("""
        <script>
            // Locate elements
            var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
            var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];
            // Observe sidebar size
            function outputsize() {
                decoration.style.left = `${sidebar.offsetWidth}px`;
            }
            new ResizeObserver(outputsize).observe(sidebar);
            // Adjust sizes
            outputsize();
            decoration.style.height = "3.0rem";
            decoration.style.right = "45px";
            // Adjust text decorations
            decoration.style.fontWeight = "bold";
            decoration.style.color = "#d5df39"; // Add this line to change the font color
            decoration.style.fontSize = "20px"; // Add this line to increase the font size
            decoration.style.display = "flex";
            decoration.style.justifyContent = "center";
            decoration.style.alignItems = "center";
            //decoration.style.fontWeight = "bold";
            decoration.style.backgroundImage = "none"; // Remove background image
            //decoration.style.backgroundSize = "unset"; // Remove background size
        </script>
    """, width=0, height=0)
    




def subHeader(text, color='white', divider=False):
    st.markdown(f"<h2 style='color:{color};'>{text}</h1>", unsafe_allow_html=True)
    if divider:
        st.markdown(f"<hr style='border:1px solid {divider};'/>", unsafe_allow_html=True)
