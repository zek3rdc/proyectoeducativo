import streamlit as st
import pandas as pd
from modulos.main_Componentes import componente_asistencias_prof
import datetime

def mostrar():
    # Obtener roles y personal
    roles = componente_asistencias_prof.obtener_roles()
    personal = componente_asistencias_prof.obtener_personal()

    if not roles:
        st.warning("No se encontraron roles disponibles.")
        return

    if not personal:
        st.warning("No se encontró personal registrado.")
        return

    st.success("Datos cargados correctamente. ¡Continúa!")


    # Tabs de asistencia
    tab1, tab2 = st.tabs(["Registrar Asistencia", "Ver Asistencias"])

    # ------------------------ REGISTRAR ASISTENCIA ------------------------
    with tab1:
        st.subheader("Registrar Asistencia")

        # Selección de rol
        selected_rol = st.selectbox("Selecciona un rol", options=list(roles.keys()), format_func=lambda x: roles[x], key="rol_registro")

        # Filtrar personal por rol
        personal_filtrado = [p for p in personal if p['ID_ROL'] == selected_rol]

        if not personal_filtrado:
            st.warning("No hay personal registrado para este rol.")
            return

        # Selección de personal
        personal_nombres = {p['ID_PERSONAL']: f"{p['NOMBRE_PERSONAL']} {p['APELLIDO_PERSONAL']}" for p in personal_filtrado}
        selected_personal = st.selectbox("Selecciona un miembro del personal", options=personal_nombres.keys(), format_func=lambda x: personal_nombres[x], key="personal_registro")

        # Selección de fecha
        fecha_actual = datetime.date.today()
        fecha_asistencia = st.date_input("Selecciona la fecha de asistencia", max_value=fecha_actual, key="fecha_asistencia")

        # Crear DataFrame editable para la asistencia
        lista_asistencia = [{
            'ID_PERSONAL': p['ID_PERSONAL'],
            'Personal': f"{p['NOMBRE_PERSONAL']} {p['APELLIDO_PERSONAL']}",
            'Cédula': str(p['CEDULA_PERSONAL']),
            'Asistió': False,
            'Justificación': False
        } for p in personal_filtrado]

        df_asistencia = pd.DataFrame(lista_asistencia)

        edited_df = st.data_editor(
            df_asistencia,
            column_config={
                "Personal": "Personal",
                "Asistió": st.column_config.CheckboxColumn("Asistió", help="Marque si asistió"),
                "Justificación": st.column_config.CheckboxColumn("Justificación", help="Marque si tiene justificación"),
                "ID_PERSONAL": None
            },
            hide_index=True,
            disabled=["Personal", "Cédula"],
            use_container_width=True
        )

        if st.button("Registrar asistencia"):
            if not edited_df.empty:
                resultados = []

                for _, row in edited_df.iterrows():
                    resultado = componente_asistencias_prof.registrar_asistencia_personal(
                        row['ID_PERSONAL'], fecha_asistencia, row['Asistió'], row['Justificación']
                    )
                    resultados.append(resultado)

                if all(resultados):
                    st.success(f"Asistencia registrada para {len(edited_df)} miembros del personal")
                else:
                    st.error("Hubo problemas con algunos registros.")

            else:
                st.warning("No hay personal en la lista de asistencia.")

    # ------------------------ VER ASISTENCIAS ------------------------
    with tab2:
        st.subheader("Ver Asistencias")

        # Selección de rol
        selected_rol_ver = st.selectbox("Selecciona un rol", options=list(roles.keys()), format_func=lambda x: roles[x], key="rol_ver")

        # Filtrar personal por rol
        personal_filtrado_ver = [p for p in personal if p['ID_ROL'] == selected_rol_ver]

        if not personal_filtrado_ver:
            st.warning("No hay personal registrado para este rol.")
            return

        # Selección de rango de fechas
        fecha_inicio = st.date_input("Selecciona la fecha de inicio", value=datetime.date.today() - datetime.timedelta(weeks=1), key="fecha_inicio_ver")
        fecha_fin = st.date_input("Selecciona la fecha de fin", value=datetime.date.today(), key="fecha_fin_ver")

        # Obtener las asistencias de todo el personal del rol seleccionado
        asistencias_personal = componente_asistencias_prof.obtener_asistencias_por_rol(selected_rol_ver, fecha_inicio, fecha_fin)

        if asistencias_personal.empty:
            st.warning("No se encontraron asistencias registradas.")
        else:
            # Mapear la cédula del personal
            # Crear un diccionario de personal con ID_PROF como clave y CEDULA_PROF como valor
            personal_dict = {p.get("ID_PROF", "No disponible"): p.get("CEDULA_PROF", "No disponible") for p in personal}

            # Ahora, agregar la Cédula a asistencias_personal utilizando el diccionario
            asistencias_personal["Cédula"] = asistencias_personal["ID_PROF"].map(personal_dict).fillna("No encontrado")

            # Renombrar columnas para visualización
            asistencias_personal.rename(columns={
                "NOMBRE_PROF": "Nombre",
                "APELLIDO_PROF": "Apellido",
                "FECHA_ASISTENCIA": "Fecha",
                "ESTADO_ASISTENCIA": "Asistió",
                "JUSTIFICACION": "Justificación"
            }, inplace=True)

            # Crear DataFrame editable
            edited_df = st.data_editor(
                asistencias_personal[["Cédula", "Nombre", "Apellido", "Fecha", "Asistió", "Justificación"]],
                column_config={
                    "Asistió": st.column_config.CheckboxColumn("Asistió", help="Marque si asistió"),
                    "Justificación": st.column_config.CheckboxColumn("Justificación", help="Marque si tiene justificación"),
                },
                hide_index=True,
                disabled=["Cédula", "Nombre", "Apellido", "Fecha"],
                use_container_width=True
            )

            # Botón para guardar cambios
            if st.button("Guardar Cambios"):
                cambios_realizados = False

                for index, row in edited_df.iterrows():
                    id_profesor = asistencias_personal.at[index, "ID_PROF"]
                    fecha_asistencia = asistencias_personal.at[index, "Fecha"]
                    estado_asistencia = row["Asistió"]
                    justificacion = row["Justificación"]

                    # Llamar a la función para actualizar en la base de datos
                    resultado = componente_asistencias_prof.actualizar_asistencia_profesor(
                        id_profesor, fecha_asistencia, estado_asistencia, justificacion
                    )
                    
                    if resultado:
                        cambios_realizados = True

                if cambios_realizados:
                    st.success("Asistencias actualizadas correctamente.")
                else:
                    st.warning("No se realizaron cambios.")

        # Botón para borrar asistencias
