import streamlit as st
from modulos import db_conector
import pandas as pd
from modulos import CrearTablas
from modulos.main_Componentes import componentes_secciones
from modulos.main_Componentes import grafico_lineal
from modulos import CrearTablas
from streamlit_extras.metric_cards import style_metric_cards


def mostrar():
    """
    Muestra la interfaz de usuario para el módulo de Secciones.

    Selecciona una opción para realizar una acción:
    - Ver Secciones: Muestra la lista de secciones existentes.
    - Agregar Nueva Sección: Abre un formulario para agregar una nueva sección.
    - Editar Sección: Abre un formulario para editar una sección existente.
    - Monitorear Sección: Muestra detalles de la sección seleccionada.
    """
    st.header("Módulo de Secciones")
    
    # Subtítulo y descripción


    # Opciones de navegación
    opcion = st.sidebar.selectbox(
        "Selecciona una opción",
        ["Ver Secciones", "Agregar Nueva Sección", "Editar Sección", "Monitorear Sección"]
    )
    
    if opcion == "Ver Secciones":
        ver_secciones()
    elif opcion == "Agregar Nueva Sección":
        agregar_seccion()
    elif opcion == "Editar Sección":
        editar_seccion()
    elif opcion == "Monitorear Sección":
        monitorear_seccion()

        
#funcion para ver secciones
def ver_secciones():
    """
    Muestra una lista de secciones existentes con opciones de filtrado por grado.

    La función obtiene las secciones de la base de datos y las muestra en un 
    DataFrame de Streamlit. Incluye un sidebar que permite filtrar las secciones
    por grado. Si no hay secciones disponibles, muestra un mensaje informativo.

    Utiliza:
    - `db_conector.obtener_secciones()` para obtener las secciones de la base de datos.
    - `crear_dataframe_secciones()` para construir el DataFrame con los datos obtenidos.

    Filtrado:
    - Permite al usuario seleccionar un grado específico para filtrar las secciones.
    - La opción "Todos" permite mostrar todas las secciones sin filtrado.

    Interface:
    - Subtítulo "Listado de Secciones".
    - Sidebar para selección de grado.
    - DataFrame mostrando las secciones disponibles.
    """
    st.subheader("Listado de Secciones")
    
    # Obtener las secciones desde la base de datos
    secciones = db_conector.obtener_secciones()
    
    if secciones:
        # Crear una lista de diccionarios con los datos de las secciones
        secciones_data = [
            {
                "ID": seccion[0],
                "Nombre": seccion[1],
                "Grado": seccion[2],
                "Profesor": seccion[3]  # Solo acceder a seccion[3] ya que contiene nombre, apellido y cédula
            }
            for seccion in secciones
        ]
        
        # Definir los nombres de las columnas
        columnas = ["ID", "Nombre", "Grado", "Profesor"]
        
        # Crear el DataFrame utilizando la función definida
        df_secciones = CrearTablas.crear_dataframe(secciones_data, columnas)
        
        # Sidebar para filtrar por grado
        st.sidebar.subheader("Filtrar Secciones")
        
        # Obtener la lista de grados únicos
        grados_unicos = df_secciones["Grado"].unique()
        grados_unicos = ["Todos"] + list(grados_unicos)  # Agregar opción para mostrar todos los grados
        
        # Seleccionar grado en el sidebar
        grado_seleccionado = st.sidebar.selectbox("Selecciona un grado", grados_unicos)
        
        # Filtrar el DataFrame por el grado seleccionado
        if grado_seleccionado != "Todos":
            df_secciones = df_secciones[df_secciones["Grado"] == grado_seleccionado]
        
        # Mostrar el DataFrame filtrado
        st.dataframe(df_secciones)
    else:
        st.write("No hay secciones disponibles.")


def agregar_seccion():
    
    """
    Muestra un formulario para agregar una nueva sección.
    
    La función muestra un formulario con los siguientes campos:
    - Nombre de la Sección (text input)
    - Seleccionar Grado (selectbox con los grados existentes)
    - Seleccionar Profesor (selectbox con los profesores existentes)
    
    Cuando se envía el formulario, se intenta agregar la nueva sección en la base de datos
    utilizando la función `agregar_seccion_db()` de `componentes_secciones`. Si la
    inserción es exitosa, se muestra un mensaje de éxito. De lo contrario, se muestra
    un mensaje de error.
    
    Interface:
    - Subtítulo "Agregar Nueva Sección"
    - Formulario con los campos mencionados
    - Botón "Agregar Sección" para enviar el formulario
    """
    st.subheader("Agregar Nueva Sección")
    
    # Formulario para agregar una nueva sección
    with st.form("form_agregar_seccion"):
        nombre_seccion = st.text_input("Nombre de la Sección")
        
        # Obtener los grados y profesores existentes para el selectbox
        grados = componentes_secciones.obtener_grados()  # Esta función debe retornar los grados existentes
        grados_nombres = [grado[1] for grado in grados]  # Solo los nombres de los grados
        
        grado_seleccionado = st.selectbox("Selecciona el Grado", grados_nombres)
        
        profesores = componentes_secciones.obtener_profesores()  # Esta función debe retornar los profesores existentes
        profesores_nombres = [f"{prof[1]} {prof[2]} {prof[3]}" for prof in profesores]  # Concatenar nombre y apellido
        
        profesor_seleccionado = st.selectbox("Seleccionar Profesor", profesores_nombres)

        submitted = st.form_submit_button("Agregar Sección")
        
        if submitted:
            try:
                # Verificar que los campos no estén vacíos
                if not nombre_seccion:
                    st.error("El nombre de la sección no puede estar vacío.")
                    return
                
                if grado_seleccionado not in grados_nombres:
                    st.error("Por favor, selecciona un grado válido.")
                    return
                
                if profesor_seleccionado not in profesores_nombres:
                    st.error("Por favor, selecciona un profesor válido.")
                    return

                # Obtener los ID del grado y profesor seleccionados
                grado_id = next(grado[0] for grado in grados if grado[1] == grado_seleccionado)
                profesor_id = next(prof[0] for prof in profesores if f"{prof[1]} {prof[2]} {prof[3]}" == profesor_seleccionado)
                
                # Llamar a la función para insertar la nueva sección en la base de datos
                if componentes_secciones.agregar_seccion_db(nombre_seccion, grado_id, profesor_id):
                    st.success(f"Sección '{nombre_seccion}' agregada exitosamente.")
                else:
                    st.error("Hubo un error al agregar la sección.")
            
            except Exception as e:
                st.error(f"Error al agregar la sección: {e}")


def editar_seccion():
    st.subheader("Editar Sección")
    
    # Obtener las secciones desde la base de datos
    secciones = db_conector.obtener_secciones()  # Asumimos que esta función obtiene las secciones
    
    if not secciones:
        st.error("No se encontraron secciones para editar.")
        return
    
    # Seleccionar la sección a editar
    seccion_seleccionada = st.selectbox("Seleccionar Sección a Editar", [seccion[1] for seccion in secciones])  # Usamos el nombre de la sección
    
    # Obtener los detalles de la sección seleccionada
    seccion_data = next(seccion for seccion in secciones if seccion[1] == seccion_seleccionada)


    
    # Mostrar los datos actuales de la sección
    with st.form("form_editar_seccion"):
        nuevo_nombre = st.text_input("Nuevo Nombre de la Sección", value=seccion_data[1])
        
        # Obtener los grados y profesores existentes para los selectbox
        grados = componentes_secciones.obtener_grados()  # Esta función retorna los grados existentes
        grados_nombres = [grado[1] for grado in grados]
        nuevo_grado = st.selectbox("Nuevo Grado", grados_nombres, index=grados_nombres.index(seccion_data[2]))
        
        # Obtener los profesores con su cédula
        profesores = componentes_secciones.obtener_profesores()  # Esta función retorna los profesores existentes
        # Modificar la lista para que incluya el nombre completo junto con la cédula
        profesores_nombres = [f"{prof[1]} {prof[2]} ({prof[3]})" for prof in profesores]
        
        # Verificar si el profesor actual se encuentra en la lista de profesores
        # Actualizar el índice en base a la estructura real de seccion_data
        profesor_actual = f"{seccion_data[3]}"  # Suponemos que seccion_data[3] es el nombre del profesor y seccion_data[4] es la cédula del profesor
        
        if profesor_actual in profesores_nombres:
            nuevo_profesor = st.selectbox("Nuevo Profesor", profesores_nombres, index=profesores_nombres.index(profesor_actual))
        else:
            # Si no se encuentra, seleccionar un valor por defecto (el primer valor en la lista)
            nuevo_profesor = st.selectbox("Nuevo Profesor", profesores_nombres)
            st.warning(f"El profesor actual no se encuentra en la lista, se seleccionó el primero por defecto.")
        
        submitted = st.form_submit_button("Actualizar Sección")
        
        if submitted:
            try:
                # Obtener los ID del grado y profesor seleccionados
                grado_id = next(grado[0] for grado in grados if grado[1] == nuevo_grado)
                
                # Extraer el ID del profesor a partir del nombre y cédula seleccionados
                nombre_profesor = nuevo_profesor.split(" (")[0]
                cedula_profesor = nuevo_profesor.split(" (")[1][:-1]  # Extraemos la cédula, eliminando el paréntesis final
                
                # Buscar el ID del profesor según el nombre y la cédula
                profesor_id = next(prof[0] for prof in profesores if f"{prof[1]} {prof[2]} ({prof[3]})" == nuevo_profesor)
                
                # Llamar a la función para actualizar la sección en la base de datos
                if componentes_secciones.editar_seccion_db(seccion_data[0], nuevo_nombre, grado_id, profesor_id):  # seccion_data[0] es el ID de la sección
                    st.success(f"Sección '{nuevo_nombre}' actualizada exitosamente.")
                else:
                    st.error("Hubo un error al actualizar la sección.")
            
            except Exception as e:
                st.error(f"Error al actualizar la sección: {e}")



def monitorear_seccion():
    st.subheader("Monitorear Sección")

    # Obtener las secciones
    secciones = db_conector.listar_secciones()
    if not secciones:
        st.write("No hay secciones disponibles.")
        return

    # Campo de búsqueda
    busqueda = st.text_input("Buscar sección por nombre")

    # Botón de búsqueda
    buscar = st.button("Buscar")

    # Si se presiona el botón de búsqueda
    if buscar:
        # Filtrar las secciones basadas en la búsqueda
        secciones_filtradas = [s for s in secciones if busqueda.lower() in s['nombre_seccion'].lower()]
    else:
        secciones_filtradas = secciones

    # Crear lista con nombres y sus respectivos IDs de las secciones filtradas
    opciones = [f"{s['nombre_seccion']} (ID: {s['id_seccion']})" for s in secciones_filtradas]

    if not opciones:
        st.write("No se encontraron secciones que coincidan con la búsqueda.")
        # Botón para volver a mostrar todas las secciones
        volver = st.button("Volver a todas las secciones")
        if volver:
            st.experimental_rerun()  # Vuelve a ejecutar la función y muestra todas las secciones
        return

    # Selección de sección
    seccion_seleccionada = st.selectbox("Seleccionar Sección para Monitorear", opciones)

    # Extraer el ID de la sección seleccionada
    id_seccion_seleccionada = int(seccion_seleccionada.split(" (ID: ")[1].replace(")", ""))

    # Buscar la información completa de la sección seleccionada por su ID
    seccion_info = next(s for s in secciones if s['id_seccion'] == id_seccion_seleccionada)

    # Mostrar información con st.columns y st.metric
    col1, col2, col3 = st.columns(3)  # Ajustamos las columnas

    # Mostrar el nombre de la sección, el grado y el profesor en tarjetas de métricas
    col1.metric(
        label="Sección Seleccionada",
        value=seccion_info['nombre_seccion'],
        delta=f"Grado: {seccion_info['grado']}"
    )

    col2.metric(
        label="Profesor",
        value=seccion_info['profesor'],
        delta="Profesor Asignado"
    )

    col3.metric(
        label="ID del Grado",
        value=str(seccion_info['grado']),
        delta="ID único del grado"
    )

    # Mostrar materias
    materias = db_conector.listar_detalles_seccion(seccion_info['id_seccion'])  # Pasar solo el ID del grado
    
    if not materias:
        st.write("No hay materias disponibles para esta sección.")
    else:
        st.write("Materias del grado:")

        # Renombrar las columnas de las materias
        materias_renombradas = componentes_secciones.rename_fields(materias)

        # Crear el DataFrame con las materias renombradas
        rename_fields = CrearTablas.crear_dataframe(materias_renombradas)

        # Mostrar el DataFrame en Streamlit
        st.dataframe(rename_fields)
