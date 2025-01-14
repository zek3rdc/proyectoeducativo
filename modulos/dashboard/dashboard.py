import streamlit as st
from modulos.Asistencias import asistencias
from modulos.Calificaciones import calificaciones
from modulos.Estudiantes import estudiantes
from modulos.Profesores import profesores
from modulos.Rendimiento import rendimiento
from modulos.secciones import secciones
from modulos.materias import materias
from modulos.grados import grados
from modulos.Representantes import representantes

def main():
    st.title("Dashboard Principal")  # Título principal

    # Aplicar estilos más discretos para tabs
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab"] {
            font-size: 16px; /* Tamaño ajustado para texto */
            padding: 8px 16px; /* Espaciado interno */
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f0f0f0; /* Color de hover */
        }
        </style>
    """, unsafe_allow_html=True)

    # Configuración de pestañas
    tab_names = ["Estudiantes", "Profesores", "Calificaciones"]
    tabs = st.tabs(tab_names)

    with tabs[0]:  # Pestaña Estudiantes
        estudiantes.dashboard()

    with tabs[1]:  # Pestaña Profesores
        profesores.dashboard()

    with tabs[2]:  # Pestaña Calificaciones
        calificaciones.dashboard()

def app():
    # Título general del aplicativo
    st.title("Sistema de Gestión Escolar")

    # Configurar barra lateral
    menu = ["Dashboard", "Calificaciones", "Asistencias", "Personal", "Estudiantes","Materias","Representantes", "Rendimiento", "Secciones","Grados"]
    opcion = st.sidebar.selectbox("Selecciona el módulo", menu)

    # Mostrar contenido según la opción seleccionada
    if opcion == "Dashboard":
        main()
    elif opcion == "Calificaciones":
        calificaciones.mostrar()
    elif opcion == "Asistencias":
        asistencias.mostrar()
    elif opcion == "Personal":
        profesores.mostrar()
    elif opcion == "Estudiantes":
        estudiantes.mostrar()
    elif opcion == "Representantes":
        representantes.mostrar()
    elif opcion == "Rendimiento":
        rendimiento.mostrar()
    elif opcion == "Secciones":
        secciones.mostrar()
    elif opcion == "Materias":
        materias.mostrar()
    elif opcion == "Grados":
        grados.mostrar()

# Llamar a la aplicación
if __name__ == "__main__":
    app()
