import streamlit as st
import pandas as pd
from modulos.main_Componentes import componente_asistencias
import time


def mostrar():
    # Obtener el ID de acceso del usuario
    # Verificar si el usuario es coordinador
    id_cordinates = st.session_state.get("coordinate")
    print(id_cordinates)

    if id_cordinates:  # Aquí evalúas si es True
        # Verificar que se tiene permisos de coordinador
        print("Usuario es coordinador, obteniendo todos los datos.")
        # Obtener todos los datos si es coordinador
        secciones = componente_asistencias.obtener_todas_las_secciones()
        estudiantes = componente_asistencias.obtener_todos_los_estudiantes()
    else:
        # Verificar si hay un ID de acceso válido
        user_id = st.session_state.get("id_acceso")
        if not user_id:
            st.error("No tienes permisos para acceder a este módulo.")
            return

        # Si no es coordinador, obtener los datos para un profesor específico
        print("Usuario no es coordinador, obteniendo datos específicos del profesor.")
        secciones = componente_asistencias.obtener_secciones(user_id)
        estudiantes = componente_asistencias.obtener_estudiantes(user_id)


        

    # Validar si hay datos en las secciones
    if not secciones or len(secciones) == 0:
        st.warning("No se encontraron secciones asignadas.")
        return

    # Validar si hay datos en las calificaciones
    if not estudiantes or len(estudiantes) == 0:
        st.warning("No se encontraron calificaciones registradas.")
        return

    # Si todo está bien, continuar con el flujo normal
    st.success("Datos cargados correctamente. ¡Continúa!")

    # Mostrar tabs para administrar asistencias
    tab1, tab2, tab3 = st.tabs(["Registrar Asistencia", "Ver Asistencias", "Modificar Asistencias"])

    with tab1:
        st.subheader("Registrar Asistencia")
        
        # Extraer los nombres de las secciones para mostrarlas en el selectbox
        secciones_nombres = [seccion['NOMBRE_SECCION'] for seccion in secciones]
        selected_seccion = st.selectbox("Selecciona una sección", secciones_nombres)

        # Obtener el ID de la sección seleccionada
        id_seccion = next(seccion['ID_SECCION'] for seccion in secciones if seccion['NOMBRE_SECCION'] == selected_seccion)
        

        # Seleccionar la fecha de asistencia (para los estudiantes)
        fecha_asistencia = st.date_input("Selecciona la fecha de asistencia", value=pd.to_datetime("today"))

        # Filtrar estudiantes por el ID_SECCION seleccionado
      # Filtrar estudiantes por el ID_SECCION seleccionado
        estudiantes_seccion = [e for e in estudiantes if e['ID_SECCION'] == id_seccion]

        print(estudiantes_seccion)

        if not estudiantes_seccion:
            st.warning(f"No hay estudiantes registrados en la sección {selected_seccion}.")
            return

        # Crear un diccionario de nombres completos a ID_EST
        nombres_estudiantes_dict = {f"{e['NOMBRE_EST']} {e['APELLIDO_EST']}": e['ID_EST'] for e in estudiantes_seccion}

        # Crear una lista de nombres completos para el multiselect
        nombres_estudiantes = list(nombres_estudiantes_dict.keys())

        # Mostrar el multiselect
        selected_estudiantes_nombres = st.multiselect("Selecciona estudiantes", nombres_estudiantes)

        # Obtener los IDs de los estudiantes seleccionados
        selected_estudiantes_ids = [nombres_estudiantes_dict[nombre] for nombre in selected_estudiantes_nombres]

        print("IDs de los estudiantes seleccionados:", selected_estudiantes_ids)

        # Registrar asistencia de los estudiantes seleccionados
        if selected_estudiantes_ids:
            if st.button("Registrar asistencia para los estudiantes seleccionados"):
                for estudiante_id in selected_estudiantes_ids:
                    resultado = componente_asistencias.registrar_asistencia_estudiante(estudiante_id, id_seccion, fecha_asistencia)
                    if resultado:
                        st.success(f"Asistencia registrada para el estudiante con ID {estudiante_id} en {fecha_asistencia}.")
                    else:
                        st.error(f"No se pudo registrar la asistencia del estudiante con ID {estudiante_id}.")

                # Aquí verificamos si el usuario tiene permisos de coordinador
                if not id_cordinates:  # Si NO es coordinador, registramos la asistencia del profesor
                    resultado_profesor = componente_asistencias.registrar_asistencia_profesor(user_id, id_seccion)
                    if resultado_profesor:
                        st.success("Asistencia del profesor registrada automáticamente.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("No se pudo registrar la asistencia del profesor.")
                else:
                    # Si es coordinador, no registramos la asistencia del profesor
                    st.success("Como coordinador, no es necesario registrar la asistencia del profesor.")




    with tab2:
        st.subheader("Ver Asistencias")
        
        # Selectbox con clave única para esta pestaña
        selected_seccion_ver = st.selectbox(
            "Selecciona una sección para ver las asistencias",
            secciones_nombres,
            key="ver_asistencias_seccion"
        )
        id_seccion_ver = next(seccion['ID_SECCION'] for seccion in secciones if seccion['NOMBRE_SECCION'] == selected_seccion_ver)
        
        # Selección de rango de fechas
        fecha_inicio = st.date_input(
            "Selecciona la fecha de inicio",
            value=pd.to_datetime("today") - pd.DateOffset(weeks=1),  # Por defecto, hace una semana
            key="ver_asistencias_fecha_inicio"
        )
        fecha_fin = st.date_input(
            "Selecciona la fecha de fin",
            value=pd.to_datetime("today"),  # Por defecto, hoy
            key="ver_asistencias_fecha_fin"
        )
        
        # Obtener asistencias para la sección y rango de fechas seleccionadas
        asistencias_estudiantes = componente_asistencias.obtener_asistencias_estudiantes(id_seccion_ver, fecha_inicio, fecha_fin)

        if asistencias_estudiantes.empty:
            st.warning(f"No se encontraron asistencias registradas para la sección {selected_seccion_ver} entre {fecha_inicio} y {fecha_fin}.")
        else:
            st.dataframe(asistencias_estudiantes)

    with tab3:
        st.subheader("Modificar Asistencias")
        
        selected_seccion_mod = st.selectbox(
            "Selecciona una sección para modificar las asistencias",
            secciones_nombres,
            key="modificar_asistencias_seccion"
        )
        id_seccion_mod = next(seccion['ID_SECCION'] for seccion in secciones if seccion['NOMBRE_SECCION'] == selected_seccion_mod)
        
        fecha_inicio_mod = st.date_input(
            "Selecciona la fecha de inicio",
            value=pd.to_datetime("today") - pd.DateOffset(weeks=1),
            key="modificar_asistencias_fecha_inicio"
        )
        fecha_fin_mod = st.date_input(
            "Selecciona la fecha de fin",
            value=pd.to_datetime("today"),
            key="modificar_asistencias_fecha_fin"
        )
        
        asistencias_estudiantes_mod = componente_asistencias.obtener_asistencias_estudiantes(id_seccion_mod, fecha_inicio_mod, fecha_fin_mod)

        if not asistencias_estudiantes_mod.empty:
            # Mostrar las asistencias en un multiselect para eliminar
            opciones_asistencias = [f"{row['NOMBRE_EST']} {row['APELLIDO_EST']} - {row['FECHA_ASISTENCIA']} - ID: {row['ID_EST']}" for index, row in asistencias_estudiantes_mod.iterrows()]
            
            # Multiselect para seleccionar asistencias a eliminar
            selected_asistencias = st.multiselect("Selecciona las asistencias a eliminar", opciones_asistencias)

            if st.button("Eliminar Asistencias"):
                for asistencia in selected_asistencias:
                    # Extraer el ID del estudiante y la fecha del texto seleccionado
                    partes = asistencia.split(" - ")
                    nombre_completo = partes[0]
                    fecha_asistencia_str = partes[1]
                    id_estudiante_str = partes[-1].split(": ")[-1]
                    
                    # Convertir a los tipos correctos
                    id_estudiante = int(id_estudiante_str)  # Convertir a entero
                    fecha_asistencia = pd.to_datetime(fecha_asistencia_str).date()  # Convertir a objeto date
                    
                    # Llamar a la función para eliminar la asistencia del estudiante en esa fecha
                    resultado_eliminacion = componente_asistencias.eliminar_asistencia_por_estudiante_y_fecha(id_estudiante, fecha_asistencia)
                    
                    if resultado_eliminacion:
                        st.success(f"Asistencia de {nombre_completo} en {fecha_asistencia} eliminada.")
                        
                        
                    else:
                        st.error(f"No se pudo eliminar la asistencia de {nombre_completo} en {fecha_asistencia}.")
            
            # Mostrar el DataFrame como un editor de datos para modificaciones
            edited_data = st.data_editor(
                asistencias_estudiantes_mod,
                column_order=['NOMBRE_EST', 'APELLIDO_EST', 'FECHA_ASISTENCIA', 'ESTADO_ASISTENCIA'],
                use_container_width=True,
                key="modificar_asistencias_editor"
            )

            if st.button("Guardar Cambios", key="guardar_cambios"):
                for index, row in edited_data.iterrows():
                    nombre_completo = f"{row['NOMBRE_EST']} {row['APELLIDO_EST']}"
                    nuevo_estado = row['ESTADO_ASISTENCIA']
                    fecha_asistencia = row['FECHA_ASISTENCIA']

                    # Actualizar el estado si no es vacío
                    resultado_mod = componente_asistencias.modificar_asistencia_estudiante(
                        nombre_completo,
                        selected_seccion_mod,
                        nuevo_estado
                    )
                    
                    if resultado_mod:
                        st.success(f"Asistencia de {nombre_completo} modificada a {nuevo_estado}.")
                    else:
                        st.error(f"No se pudo modificar la asistencia de {nombre_completo}.")
        else:
            st.warning(f"No se encontraron asistencias registradas para la sección {selected_seccion_mod} entre {fecha_inicio_mod} y {fecha_fin_mod}.")

