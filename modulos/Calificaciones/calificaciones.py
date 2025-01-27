import streamlit as st
from modulos.main_Componentes import componente_calificaciones

def mostrar():
    st.header("Módulo de Calificaciones")

    # Verificar si el usuario es coordinador
    id_cordinates = st.session_state.get("coordinate")
    print(id_cordinates)  # Asegúrate de que sea True o False
    if id_cordinates:  # Aquí evalúas si es True
        # Obtener todos los datos si es coordinador
        secciones, calificaciones = componente_calificaciones.obtener_todos_datos_calificaciones()
    else:
        # Verificar si hay un ID de acceso válido
        id_acceso = st.session_state.get("id_acceso")
        if not id_acceso:
            st.error("No tienes permisos para acceder a este módulo.")
            return

        # Obtener datos del profesor según su ID de acceso
        secciones, calificaciones = componente_calificaciones.obtener_datos_calificaciones(id_acceso)

    # Validar si hay datos en las secciones
    if not secciones or len(secciones) == 0:
        st.warning("No se encontraron secciones asignadas.")
        return

    # Validar si hay datos en las calificaciones
    if not calificaciones or len(calificaciones) == 0:
        st.warning("No se encontraron calificaciones registradas.")
        return

    # Si todo está bien, continuar con el flujo normal
    st.success("Datos cargados correctamente. ¡Continúa!")

    # Mostrar los filtros
    st.subheader("Filtros")

    # Filtro de secciones
    seccion_opciones = [seccion['NOMBRE_SECCION'] for seccion in secciones]
    seccion_filtro = st.selectbox("Filtrar por sección:", ["Todas"] + seccion_opciones)

    # Filtro de estudiantes
    estudiante_filtro = st.text_input("Buscar por nombre del estudiante:")

    # Filtro de calificaciones
    calificacion_filtro_tipo = st.radio(
        "Filtrar calificaciones:",
        ["Todas", "Superiores a", "Menores a"],
        horizontal=True
    )
    calificacion_filtro_valor = None
    if calificacion_filtro_tipo != "Todas":
        calificacion_filtro_valor = st.number_input(
            "Valor de la calificación:", min_value=0.0, max_value=100.0, step=0.5
        )

    # Filtro de materias
    materia_opciones = list(set([calificacion['NOMBRE_MATERIA'] for calificacion in calificaciones]))
    materia_filtro = st.selectbox("Filtrar por materia:", ["Todas"] + materia_opciones)

    # Filtrar las calificaciones
    calificaciones_filtradas = calificaciones
    if seccion_filtro != "Todas":
        calificaciones_filtradas = [
            calificacion for calificacion in calificaciones
            if calificacion['NOMBRE_SECCION'] == seccion_filtro
        ]

    if estudiante_filtro:
        calificaciones_filtradas = [
            calificacion for calificacion in calificaciones_filtradas
            if estudiante_filtro.lower() in (calificacion['NOMBRE_EST'] + " " + calificacion['APELLIDO_EST']).lower()
        ]

    if calificacion_filtro_valor is not None:
        if calificacion_filtro_tipo == "Superiores a":
            calificaciones_filtradas = [
                calificacion for calificacion in calificaciones_filtradas
                if calificacion['CALIFICACION'] > calificacion_filtro_valor
            ]
        elif calificacion_filtro_tipo == "Menores a":
            calificaciones_filtradas = [
                calificacion for calificacion in calificaciones_filtradas
                if calificacion['CALIFICACION'] < calificacion_filtro_valor
            ]

    if materia_filtro != "Todas":
        calificaciones_filtradas = [
            calificacion for calificacion in calificaciones_filtradas
            if calificacion['NOMBRE_MATERIA'] == materia_filtro
        ]

    # Mostrar las calificaciones en un editor
    st.subheader("Calificaciones de los Estudiantes")
    if not calificaciones_filtradas:
        st.warning("No se encontraron calificaciones con los filtros aplicados.")
        return

    # Preparar datos para edición
    calificaciones_df = {
        "ID_CALIFICACION": [calificacion['ID_CALIFICACION'] for calificacion in calificaciones_filtradas],
        "Estudiante": [f"{calificacion['NOMBRE_EST']} {calificacion['APELLIDO_EST']}" for calificacion in calificaciones_filtradas],
        "Materia": [calificacion['NOMBRE_MATERIA'] for calificacion in calificaciones_filtradas],
        "Calificación": [calificacion['CALIFICACION'] for calificacion in calificaciones_filtradas],
        "Fecha De Asignacion de Calificacion": [calificacion['FECHA_CALIFICACION'] for calificacion in calificaciones_filtradas],
    }

    # Hacer que solo la columna 'Calificación' sea editable
    calificaciones_editadas = st.data_editor(
        calificaciones_df,
        use_container_width=True,
        key="calificaciones_editor",
        disabled=["ID_CALIFICACION", "Estudiante", "Materia", "Fecha De Asignacion de Calificacion"]
    )

    # Guardar cambios en la base de datos
    if st.button("Guardar cambios"):
        cambios_realizados = False
        for idx, calificacion in enumerate(calificaciones_filtradas):
            nueva_calificacion = calificaciones_editadas["Calificación"][idx]
            if nueva_calificacion != calificacion['CALIFICACION']:
                componente_calificaciones.actualizar_calificacion(
                    calificacion['ID_CALIFICACION'], nueva_calificacion
                )
                cambios_realizados = True

        if cambios_realizados:
            st.success("Cambios guardados correctamente.")
        else:
            st.info("No se realizaron cambios.")
