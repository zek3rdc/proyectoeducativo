import streamlit as st
import pandas as pd
from modulos.main_Componentes.componente_materias import listar_materias, eliminar_materia, actualizar_materia, agregar_materia, asignar_materia_a_seccion
from modulos import db_conector

def mostrar():
    st.header("Módulo de Materias")

    menu = ["Agregar Materia", "Ver Materias", "Asignar Materia a Sección"]
    opcion = st.selectbox("Selecciona una opción", menu)

    if opcion == "Agregar Materia":
        with st.form("Agregar Materia"):
            nombre = st.text_input("Nombre de la materia")
            descripcion = st.text_area("Descripción")
            submit = st.form_submit_button("Agregar")

            if submit:
                if agregar_materia(nombre, descripcion):
                    st.success("Materia agregada exitosamente")
                else:
                    st.error("Error al agregar la materia")

    elif opcion == "Ver Materias":
        # Obtener las materias y crear el DataFrame
        materias = listar_materias()
        if materias:
            # Crear un DataFrame a partir de la lista de materias
            df = pd.DataFrame(materias)

            # Mostrar el editor de datos con el DataFrame
            df_editable = st.data_editor(df, height=600, use_container_width=True)

            # Botón para guardar los cambios
            if st.button("Guardar Cambios"):
                # Iterar sobre el DataFrame editable y actualizar la base de datos
                for index, row in df_editable.iterrows():
                    if row["NOMBRE_MATERIA"] != materias[index]["NOMBRE_MATERIA"] or row["DESCRIPCION_MATERIA"] != materias[index]["DESCRIPCION_MATERIA"]:
                        if not actualizar_materia(row["ID_MATERIA"], row["NOMBRE_MATERIA"], row["DESCRIPCION_MATERIA"]):
                            st.error(f"Error al actualizar la materia con ID: {row['ID_MATERIA']}")
                        else:
                            st.success(f"Materia con ID {row['ID_MATERIA']} actualizada exitosamente")

            # Opción para eliminar varias materias
            ids_a_eliminar = st.multiselect("Selecciona las materias a eliminar", options=[materia["NOMBRE_MATERIA"] for materia in materias])
            if st.button("Eliminar Seleccionadas"):
                for nombre_materia in ids_a_eliminar:
                    materia_a_eliminar = next((materia for materia in materias if materia["NOMBRE_MATERIA"] == nombre_materia), None)
                    if materia_a_eliminar:
                        if eliminar_materia(materia_a_eliminar["ID_MATERIA"]):
                            st.success(f"Materia {nombre_materia} eliminada exitosamente")
                        else:
                            st.error(f"Error al eliminar la materia {nombre_materia}")
        else:
            st.warning("No hay materias registradas")

    elif opcion == "Asignar Materia a Sección":
    # Cargar las materias y secciones
        # Cargar las materias y secciones
        materias = listar_materias()  # Asegúrate de que esta función retorne una lista de materias
        secciones = db_conector.obtener_secciones()  # Esta función retorna una lista de tuplas

        # Convertir la lista de tuplas de secciones a un DataFrame con nombres de columnas correctos
        df_secciones = pd.DataFrame(secciones, columns=["ID_SECCION", "NOMBRE_SECCION", "GRADO", "PROFESOR"])

        # Convertir las listas de materias a DataFrame para visualizarlas
        df_materias = pd.DataFrame(materias)

        # Crear columnas para mostrar los DataFrames uno al lado del otro
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Materias")
            st.dataframe(df_materias)

        with col2:
            st.subheader("Secciones")
            st.dataframe(df_secciones)

        # Crear multiselects debajo de los DataFrames para seleccionar grados y materias
        selected_materias = st.multiselect("Selecciona las materias", df_materias['NOMBRE_MATERIA'].tolist())
        selected_secciones = st.multiselect("Selecciona las secciones", df_secciones['NOMBRE_SECCION'].tolist())

        if st.button("Asignar"):
            # Verificar si se seleccionaron materias y secciones
            if not selected_materias or not selected_secciones:
                st.error("Por favor, selecciona al menos una materia y una sección.")
            else:
                # Asignar las materias a las secciones seleccionadas
                for materia in selected_materias:
                    for seccion in selected_secciones:
                        # Convertir los IDs a int explícitamente
                        id_materia = int(df_materias[df_materias['NOMBRE_MATERIA'] == materia].iloc[0]['ID_MATERIA'])
                        id_seccion = int(df_secciones[df_secciones['NOMBRE_SECCION'] == seccion].iloc[0]['ID_SECCION'])
                        
                        # Llamar a la función para asignar la materia a la sección
                        if asignar_materia_a_seccion(id_materia, id_seccion):
                            st.success(f"Materia '{materia}' asignada a la sección '{seccion}' exitosamente.")
                        else:
                            st.error(f"Error al asignar la materia '{materia}' a la sección '{seccion}'.")