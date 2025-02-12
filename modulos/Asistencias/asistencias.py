import streamlit as st
import pandas as pd
from modulos.main_Componentes import componente_asistencias
import time
import datetime


def mostrar():
    # Obtener el ID de acceso del usuario
    id_cordinates = st.session_state.get("coordinate")
    print(id_cordinates)

    if id_cordinates:  # Si es coordinador
        print("Usuario es coordinador, obteniendo todos los datos.")
        secciones = componente_asistencias.obtener_todas_las_secciones()
        estudiantes = componente_asistencias.obtener_todos_los_estudiantes()
    else:
        user_id = st.session_state.get("id_acceso")
        if not user_id:
            st.error("No tienes permisos para acceder a este módulo.")
            return

        print("Usuario no es coordinador, obteniendo datos específicos del profesor.")
        secciones = componente_asistencias.obtener_secciones(user_id)
        estudiantes = componente_asistencias.obtener_estudiantes(user_id)

    if not secciones:
        st.warning("No se encontraron secciones asignadas.")
        return

    if not estudiantes:
        st.warning("No se encontraron estudiantes registrados.")
        return

    st.success("Datos cargados correctamente. ¡Continúa!")

    # Obtener los grados disponibles
    grados = {grado['ID_GRADOS']: grado['NOMBRE_GRADO'] for grado in secciones}

    # Tabs de asistencia
    tab1, tab2, tab3 = st.tabs(["Registrar Asistencia", "Ver Asistencias", "Modificar Asistencias"])


    # ------------------------ REGISTRAR ASISTENCIA ------------------------
    with tab1:
        st.subheader("Registrar Asistencia")

        # Selección de grado
        selected_grado = st.selectbox("Selecciona un grado", list(grados.values()), key="grado_registro")

        # Filtrar secciones por grado
        secciones_filtradas = [s for s in secciones if s['NOMBRE_GRADO'] == selected_grado]
        secciones_nombres = [seccion['NOMBRE_SECCION'] for seccion in secciones_filtradas]
        selected_seccion = st.selectbox("Selecciona una sección", secciones_nombres, key="seccion_registro")

        id_seccion = next(seccion['ID_SECCION'] for seccion in secciones_filtradas if seccion['NOMBRE_SECCION'] == selected_seccion)
        
        fecha_actual = datetime.date.today()
        fecha_asistencia = pd.to_datetime(st.date_input("Selecciona la fecha de asistencia", max_value=fecha_actual, key="fecha_asistencia"))

        estudiantes_seccion = [e for e in estudiantes if e['ID_SECCION'] == id_seccion]

        if not estudiantes_seccion:
            st.warning(f"No hay estudiantes en la sección {selected_seccion}.")
            st.stop()

        lista_asistencia = [{
            'Estudiante': f"{e['NOMBRE_EST']} {e['APELLIDO_EST']}",
            'Cédula': str(e['CEDULA_EST']),
            'Asistió': False,
            'Justificación': False,
            'ID_EST': e['ID_EST']
        } for e in estudiantes_seccion]

        df_asistencia = pd.DataFrame(lista_asistencia)

        edited_df = st.data_editor(
            df_asistencia,
            column_config={
                "Estudiante": "Estudiante",
                "Asistió": st.column_config.CheckboxColumn("Asistió", help="Marque los estudiantes presentes"),
                "Justificación": st.column_config.CheckboxColumn("Justificación", help="Marque los estudiantes con justificación"),
                "ID_EST": None
            },
            hide_index=True,
            disabled=["Estudiante", "Cédula"],
            use_container_width=True
        )

        if st.button("Registrar asistencia"):
            if not edited_df.empty:
                resultados = []

                for _, row in edited_df.iterrows():
                    id_estudiante = row['ID_EST']
                    asistio = row['Asistió']
                    justificacion = row['Justificación']

                    resultado = componente_asistencias.registrar_asistencia_estudiante(
                        id_estudiante, id_seccion, fecha_asistencia, asistio, justificacion
                    )
                    resultados.append(resultado)

                if all(resultados):
                    st.success(f"Asistencia registrada para {len(edited_df)} estudiantes")
                else:
                    st.warning("Hubo problemas con algunos registros.")

                if not id_cordinates:
                    resultado_profesor = componente_asistencias.registrar_asistencia_profesor(user_id, id_seccion)
                    if resultado_profesor:
                        st.success("Asistencia del profesor registrada.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("No se pudo registrar la asistencia del profesor.")
                else:
                    st.success("Coordinador: No es necesario registrar asistencia del profesor.")

            else:
                st.warning("No hay estudiantes en la lista de asistencia.")


    # ------------------------ VER ASISTENCIAS ------------------------
    with tab2:
        st.subheader("Ver Asistencias")

        selected_grado_ver = st.selectbox("Selecciona un grado", list(grados.values()), key="grado_ver")

        secciones_filtradas_ver = [s for s in secciones if s['NOMBRE_GRADO'] == selected_grado_ver]
        secciones_nombres_ver = [seccion['NOMBRE_SECCION'] for seccion in secciones_filtradas_ver]
        selected_seccion_ver = st.selectbox("Selecciona una sección", secciones_nombres_ver, key="seccion_ver")

        id_seccion_ver = next(seccion['ID_SECCION'] for seccion in secciones_filtradas_ver if seccion['NOMBRE_SECCION'] == selected_seccion_ver)

        fecha_inicio = st.date_input("Selecciona la fecha de inicio", value=pd.to_datetime("today") - pd.DateOffset(weeks=1), key="fecha_inicio_ver")
        fecha_fin = st.date_input("Selecciona la fecha de fin", value=pd.to_datetime("today"), key="fecha_fin_ver")

        asistencias_estudiantes = componente_asistencias.obtener_asistencias_estudiantes(id_seccion_ver, fecha_inicio, fecha_fin)

        if asistencias_estudiantes.empty:
            st.warning("No se encontraron asistencias registradas.")
        else:
            st.dataframe(asistencias_estudiantes)


    # ------------------------ MODIFICAR ASISTENCIAS ------------------------
    with tab3:
        st.subheader("Modificar Asistencias")

        selected_grado_mod = st.selectbox("Selecciona un grado", list(grados.values()), key="grado_mod")

        secciones_filtradas_mod = [s for s in secciones if s['NOMBRE_GRADO'] == selected_grado_mod]
        secciones_nombres_mod = [seccion['NOMBRE_SECCION'] for seccion in secciones_filtradas_mod]
        selected_seccion_mod = st.selectbox("Selecciona una sección", secciones_nombres_mod, key="seccion_mod")

        id_seccion_mod = next(seccion['ID_SECCION'] for seccion in secciones_filtradas_mod if seccion['NOMBRE_SECCION'] == selected_seccion_mod)

        fecha_inicio_mod = st.date_input("Selecciona la fecha de inicio", value=pd.to_datetime("today") - pd.DateOffset(weeks=1), key="fecha_inicio_mod")
        fecha_fin_mod = st.date_input("Selecciona la fecha de fin", value=pd.to_datetime("today"), key="fecha_fin_mod")

        asistencias_estudiantes_mod = componente_asistencias.obtener_asistencias_estudiantes(id_seccion_mod, fecha_inicio_mod, fecha_fin_mod)

        if not asistencias_estudiantes_mod.empty:
            edited_data = st.data_editor(
                asistencias_estudiantes_mod,
                column_order=['NOMBRE_EST', 'APELLIDO_EST', 'FECHA_ASISTENCIA', 'ESTADO_ASISTENCIA', 'JUSTIFICACIÓN'],
                disabled=["NOMBRE_EST", "APELLIDO_EST"],  # Deshabilitar nombres de estudiantes
                use_container_width=True,
                key="modificar_asistencias_editor"
            )

            if st.button("Guardar Cambios"):
                for index, row in edited_data.iterrows():
                    resultado_mod = componente_asistencias.modificar_asistencia_estudiante(
                        row['ID_EST'],
                        id_seccion_mod,
                        row['ESTADO_ASISTENCIA'],
                        row['JUSTIFICACIÓN']  # Ahora se incluye justificación
                    )

                    if resultado_mod:
                        st.success("Asistencia modificada.")
                    else:
                        st.error("Error al modificar asistencia.")
        else:
            st.warning("No se encontraron asistencias registradas.")
