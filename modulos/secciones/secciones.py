import streamlit as st
from modulos import db_conector
import pandas as pd
from modulos import CrearTablas
from modulos.main_Componentes import componentes_secciones
import time


def mostrar():
    """
    Muestra la interfaz de usuario para el módulo de Secciones utilizando pestañas.
    """
    st.header("Módulo de Secciones")

    # Crear pestañas
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Ver Secciones", "➕ Agregar Sección", "✏️ Editar Sección", "📊 Monitorear Sección"])

    with tab1:
        ver_secciones()

    with tab2:
        agregar_seccion()

    with tab3:
        editar_seccion()

    with tab4:
        monitorear_seccion()


def ver_secciones():
    """Muestra una lista de secciones con opciones de filtrado."""
    st.subheader("Listado de Secciones")
    secciones = db_conector.obtener_secciones()
    
    if secciones:
        secciones_data = [{"ID": sec[0], "Nombre": sec[1], "Grado": sec[2], "Profesor": sec[3]} for sec in secciones]
        df_secciones = CrearTablas.crear_dataframe(secciones_data, ["ID", "Nombre", "Grado", "Profesor"])

        # Sidebar para filtros
        st.sidebar.subheader("Filtrar")
        grados_unicos = ["Todos"] + list(df_secciones["Grado"].unique())
        grado_seleccionado = st.sidebar.selectbox("Selecciona un grado", grados_unicos)

        if grado_seleccionado != "Todos":
            df_secciones = df_secciones[df_secciones["Grado"] == grado_seleccionado]

        secciones_unicas = ["Todas"] + list(df_secciones["Nombre"].unique())
        seccion_seleccionada = st.sidebar.selectbox("Selecciona una sección", secciones_unicas)

        if seccion_seleccionada != "Todas":
            id_seccion = df_secciones[df_secciones["Nombre"] == seccion_seleccionada]["ID"].values[0]
            estudiantes = db_conector.obtener_estudiantes_por_seccion(id_seccion)
            
            if estudiantes:
                df_estudiantes = pd.DataFrame(estudiantes, columns=["ID", "Nombre", "Apellido", "Cédula", "Cedula Estudiantil"])
                st.dataframe(df_estudiantes, use_container_width=True)
            else:
                st.write(f"No hay estudiantes en la sección **{seccion_seleccionada}**.")
        else:
            st.dataframe(df_secciones, use_container_width=True)
    else:
        st.write("No hay secciones disponibles.")


def agregar_seccion():
    """Formulario para agregar una nueva sección."""
    st.subheader("Agregar Nueva Sección")
    grados = componentes_secciones.obtener_grados()
    grados_nombres = [grado[1] for grado in grados]
    roles = componentes_secciones.obtener_roles()
    roles_nombres = [rol[1] for rol in roles if len(rol[1]) > 2]

    rol_seleccionado = st.selectbox("Seleccionar Cargo", roles_nombres, index=0)
    personal = componentes_secciones.obtener_personal_por_rol(rol_seleccionado) if rol_seleccionado else []
    personal_nombres = [f"{pers[1]} {pers[2]} - {pers[3]}" for pers in personal] if personal else ["No hay personal disponible"]
    profesor_seleccionado = st.selectbox("Seleccionar Personal", personal_nombres)

    with st.form("form_agregar_seccion"):
        nombre_seccion = st.text_input("Nombre de la Sección")
        grado_seleccionado = st.selectbox("Selecciona el Grado", grados_nombres)
        submitted = st.form_submit_button("Agregar Sección")

        if submitted:
            if not nombre_seccion or grado_seleccionado not in grados_nombres or profesor_seleccionado == "No hay personal disponible":
                st.error("Todos los campos son obligatorios.")
                return

            grado_id = next(grado[0] for grado in grados if grado[1] == grado_seleccionado)
            profesor_id = next(pers[0] for pers in personal if f"{pers[1]} {pers[2]} - {pers[3]}" == profesor_seleccionado)

            if componentes_secciones.agregar_seccion_db(nombre_seccion, grado_id, profesor_id):
                st.success(f"Sección '{nombre_seccion}' agregada exitosamente.")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Error al agregar la sección.")


def editar_seccion():
    """Formulario para editar una sección existente."""
    st.subheader("Editar Sección")
    secciones = db_conector.obtener_secciones()

    if not secciones:
        st.error("No se encontraron secciones para editar.")
        return

    seccion_seleccionada = st.selectbox("Seleccionar Sección a Editar", [sec[1] for sec in secciones])
    seccion_data = next(sec for sec in secciones if sec[1] == seccion_seleccionada)

    grados = componentes_secciones.obtener_grados()
    grados_nombres = [grado[1] for grado in grados]
    nuevo_grado = st.selectbox("Nuevo Grado", grados_nombres, index=grados_nombres.index(seccion_data[2]))

    roles = componentes_secciones.obtener_roles()
    roles_nombres = [rol[1] for rol in roles if len(rol[1]) > 2]
    rol_seleccionado = st.selectbox("Seleccionar Cargo", roles_nombres, index=0,key='rol')

    personal = componentes_secciones.obtener_personal_por_rol(rol_seleccionado) if rol_seleccionado else []
    personal_nombres = [f"{pers[1]} {pers[2]} - {pers[3]}" for pers in personal] if personal else ["No hay personal disponible"]
    nuevo_profesor_completo = st.selectbox("Nuevo Personal", personal_nombres)

    with st.form("form_editar_seccion"):
        nuevo_nombre = st.text_input("Nuevo Nombre de la Sección", value=seccion_data[1])
        submitted = st.form_submit_button("Actualizar Sección")

        if submitted:
            nuevo_grado_id = next(grado[0] for grado in grados if grado[1] == nuevo_grado)
            nuevo_profesor_id = next((pers[0] for pers in personal if f"{pers[1]} {pers[2]} - {pers[3]}" == nuevo_profesor_completo), None)

            if not nuevo_profesor_id:
                st.error("Selecciona un miembro del personal válido.")
                return

            if componentes_secciones.editar_seccion_db(seccion_data[0], nuevo_nombre, nuevo_grado_id, nuevo_profesor_id):
                st.success("Sección actualizada exitosamente.")
            else:
                st.error("No se pudo actualizar la sección.")


def monitorear_seccion():
    """Monitoreo de secciones con métricas y materias."""
    st.subheader("Monitorear Sección")
    secciones = db_conector.listar_secciones()
    if not secciones:
        st.write("No hay secciones disponibles.")
        return

    busqueda = st.text_input("Buscar sección por nombre")
    buscar = st.button("Buscar")
    secciones_filtradas = [s for s in secciones if busqueda.lower() in s['nombre_seccion'].lower()] if buscar else secciones
    opciones = [f"{s['nombre_seccion']} (ID: {s['id_seccion']})" for s in secciones_filtradas]

    if not opciones:
        st.write("No se encontraron secciones.")
        return

    seccion_seleccionada = st.selectbox("Seleccionar Sección para Monitorear", opciones)
    id_seccion = int(seccion_seleccionada.split(" (ID: ")[1].replace(")", ""))
    seccion_info = next(s for s in secciones if s['id_seccion'] == id_seccion)

    col1, col2, col3 = st.columns(3)
    col1.metric("Sección", seccion_info['nombre_seccion'], f"Grado: {seccion_info['grado']}")
    col2.metric("Profesor", seccion_info['profesor'])
    col3.metric("ID del Grado", str(seccion_info['grado']))

    materias = db_conector.listar_detalles_seccion(id_seccion)
    if materias:
        st.dataframe(CrearTablas.crear_dataframe(componentes_secciones.rename_fields(materias)))
    else:
        st.write("No hay materias disponibles para esta sección.")
