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

def main(user_permissions):
    st.title("Dashboard Principal")

    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            padding: 8px 16px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    tab_names = [tab for tab in ["Estudiantes", "Profesores", "Calificaciones"] if tab in user_permissions]
    if tab_names:
        tabs = st.tabs(tab_names)

        for i, tab_name in enumerate(tab_names):
            with tabs[i]:
                if tab_name == "Estudiantes":
                    estudiantes.dashboard()
                elif tab_name == "Profesores":
                    profesores.dashboard()
                elif tab_name == "Calificaciones":
                    calificaciones.dashboard()

def app(user_permissions):
    st.title("Sistema de Gestión Escolar")

    menu = [option for option in ["Dashboard", "Calificaciones", "Asistencias", "Personal", "Estudiantes", "Materias", "Representantes", "Rendimiento", "Secciones", "Grados"] if option in user_permissions]
    
    if menu:
        opcion = st.sidebar.selectbox("Selecciona el módulo", menu)

        if opcion == "Dashboard":
            main(user_permissions)
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
    else:
        st.warning("No tienes permisos para acceder a ningún módulo.")

