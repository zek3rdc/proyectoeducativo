import streamlit as st
import pandas as pd
from modulos import db_conector  # Asegúrate de que este archivo esté correctamente configurado

def convertir_a_letra(calificacion):
    """
    Convierte una calificación numérica a su equivalente en letras.
    Basado en el sistema venezolano:
    - 18-20: A
    - 15-17: B
    - 12-14: C
    - 10-11: D
    - <10: F
    """
    if calificacion >= 18:
        return "A"
    elif calificacion >= 15:
        return "B"
    elif calificacion >= 12:
        return "C"
    elif calificacion >= 10:
        return "D"
    else:
        return "F"

def mostrar():
    """
    Módulo de Rendimiento Académico.
    """
    st.header("Módulo de Rendimiento Académico")
    st.write("Consulta y análisis del rendimiento académico de los estudiantes.")

    # Filtros
    secciones = ["Ver Todo"] + db_conector.obtener_secciones_rendimiento()
    materias = ["Ver Todo"] + db_conector.obtener_materias()
    year_escolar = ["Ver Todo"] + db_conector.obtener_anios_escolares()

    st.sidebar.header("Filtros")
    filtro_seccion = st.sidebar.selectbox("Selecciona una sección", secciones, index=0)
    filtro_materia = st.sidebar.selectbox("Selecciona una materia", materias, index=0)
    filtro_year = st.sidebar.selectbox("Selecciona un año escolar", year_escolar, index=0)

    # Consulta de datos
    calificaciones = db_conector.obtener_calificaciones(filtro_seccion, filtro_materia, filtro_year)

    if calificaciones.empty:
        st.warning("No se encontraron datos para los filtros seleccionados.")
        return

    # Convertir calificaciones numéricas a letras
    calificaciones['LETRA'] = calificaciones['CALIFICACION'].apply(convertir_a_letra)

    # Mostrar datos en una tabla
    st.subheader("Calificaciones de los Estudiantes")
    st.dataframe(calificaciones)

    # Análisis del rendimiento
    st.subheader("Análisis del Rendimiento")
    promedio = calificaciones['CALIFICACION'].mean()
    mejor_calificacion = calificaciones['CALIFICACION'].max()
    peor_calificacion = calificaciones['CALIFICACION'].min()

    st.write(f"Promedio General: **{promedio:.2f}** ({convertir_a_letra(promedio)})")
    st.write(f"Mejor Calificación: **{mejor_calificacion}** ({convertir_a_letra(mejor_calificacion)})")
    st.write(f"Peor Calificación: **{peor_calificacion}** ({convertir_a_letra(peor_calificacion)})")

    # Estudiantes destacados y con bajo rendimiento
    st.subheader("Estudiantes Destacados")
    destacados = calificaciones[calificaciones['CALIFICACION'] >= 18]
    st.write("Estudiantes con calificaciones de 'A' (18-20 puntos):")
    st.dataframe(destacados)

    st.subheader("Estudiantes con Bajo Rendimiento")
    bajos = calificaciones[calificaciones['CALIFICACION'] < 10]
    st.write("Estudiantes con calificaciones de 'F' (menores a 10 puntos):")
    st.dataframe(bajos)
