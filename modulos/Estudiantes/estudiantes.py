import streamlit as st
from modulos import db_conector
from modulos.main_Componentes import Componentes_estudiantes  # Asegúrate de que la ruta sea correcta
from modulos import CrearTablas

def mostrar():
    st.header("Módulo de Estudiantes")

    # Obtener la lista de estudiantes y padres
    estudiantes = db_conector.obtener_estudiantes_1()
    padres = db_conector.obtener_padres()  
    estudiantes_dict = {f"{est['NOMBRE_EST']} {est['APELLIDO_EST']} - Cédula Estudiantil: {est['CI_EST']} (ID: {est['ID_ESTUDIANTE']})": est for est in estudiantes}
    padres_dict = {f"{padre['NOMBRE_REPRE']} {padre['APELLIDO_REPRE']} - Cédula: {padre['CEDULA_REPRE']} (ID: {padre['ID_REPRESENTANTES']})": padre['ID_REPRESENTANTES'] for padre in padres}

    # Crear pestañas
    tab2, tab3, tab4, tab5 = st.tabs(["Agregar Estudiante", "Modificar Estudiante", "Cambiar estado Estudiante", "Lista de Estudiantes"])

    # Crear un DataFrame a partir de los estudiantes
    df_estudiantes = CrearTablas.crear_dataframe(estudiantes)
    df_estudiantes = Componentes_estudiantes.renombrar_columnas(df_estudiantes)

    # Pestaña de Agregar Estudiante
    with tab2:
        st.subheader("Agregar Estudiante")  
        nombre = st.text_input("Nombre", key="nombre_input_agregar")
        apellido = st.text_input("Apellido", key="apellido_input_agregar")
        matricula = st.text_input("Matrícula", key="matricula_input_agregar")
        cedula = st.text_input("Cédula", key="cedula_input_agregar")
        genero = st.selectbox("Género", ["varon", "hembra"], key="genero_input_agregar")
        
        padre_seleccionado = st.selectbox("Seleccionar Padre", list(padres_dict.keys()), key="padre_input_agregar")
        
        if st.button("Agregar Estudiante", key="agregar_estudiante"):
            if not matricula:
                st.error("La matrícula no puede estar vacía.")
            else:
                # Verificar si la matrícula y cédula ya existen
                if db_conector.matricula_existe(matricula):
                    st.error("La cédula estudiantil ya existe. Por favor, ingresa una cédula estudiantil única.")
                elif db_conector.cedula_existe(cedula):
                    st.error("La cédula ya existe. Por favor, ingresa una cédula única.")
                else:
                    id_padre = padres_dict[padre_seleccionado]
                    id_nuevo_estudiante = Componentes_estudiantes.agregar_estudiante(nombre, apellido, matricula, cedula, id_padre, genero)
                    st.success("Estudiante agregado y vinculado al padre exitosamente")

    # Pestaña de Modificar Estudiante
    with tab3:
        st.subheader("Modificar Estudiante")
        
        # Mostrar el DataFrame de estudiantes antes de modificar
        st.write("Lista de Estudiantes")
        st.dataframe(df_estudiantes)

        estudiante_seleccionado = st.selectbox("Seleccionar Estudiante para Modificar", list(estudiantes_dict.keys()), key="select_estudiante_modificar")
        
        if estudiante_seleccionado:
            est_data = estudiantes_dict[estudiante_seleccionado]
            
            # Asegúrate de que est_data contenga las claves correctas
            nuevo_nombre = st.text_input("Nuevo Nombre", value=est_data['NOMBRE_EST'], key="nuevo_nombre_input_modificar")
            nuevo_apellido = st.text_input("Nuevo Apellido", value=est_data['APELLIDO_EST'], key="nuevo_apellido_input_modificar")
            nueva_matricula = st.text_input("Nueva Matrícula", value=est_data['CI_EST'], key="nueva_matricula_input_modificar")
            nueva_cedula = st.text_input("Nueva Cédula", value=est_data['CEDULA_EST'], key="nueva_cedula_input_modificar")

            if st.button("Modificar Estudiante", key="modificar_estudiante"):
                # Llama a la función modificando la llamada para pasar el diccionario completo
                Componentes_estudiantes.modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula)
                st.success("Estudiante modificado exitosamente")

    # Pestaña de Cambiar Estado de Estudiante
    with tab4:
        st.subheader("Cambiar Estado de Estudiante")

        # Mostrar el DataFrame de estudiantes antes de cambiar el estado
        st.write("Lista de Estudiantes")
        st.dataframe(df_estudiantes)

        # Cambiar el selectbox a un multiselect
        estudiantes_a_modificar = st.multiselect("Seleccionar Estudiantes", list(estudiantes_dict.keys()), key="estudiantes_a_modificar")

        # Selector para el nuevo estado
        nuevo_estado = st.selectbox("Nuevo Estado", ["Activo", "Inactivo", "Retirado", "Expulsado", "Graduado"], key="nuevo_estado_input")

        # Campos adicionales para la descripción del cambio
        descripcion = st.text_input("Descripción del Cambio", "Cambio de estado en el sistema.", key="descripcion_input")
        
        if estudiantes_a_modificar and nuevo_estado and descripcion:
            ids_a_modificar = [estudiantes_dict[estudiante]['ID_ESTUDIANTE'] for estudiante in estudiantes_a_modificar]

            # Botón para confirmar el cambio de estado
            if st.button("Cambiar Estado de Estudiantes", key="cambiar_estado_input"):
                for est_id in ids_a_modificar:
                    # Llamada a la función en `Componentes_estudiantes` para cambiar el estado y registrar el cambio
                    Componentes_estudiantes.cambiar_estado_estudiante(est_id, nuevo_estado, descripcion)
                st.success("Estado de estudiantes actualizado correctamente.")
    # Pestaña de Lista de Estudiantes
    with tab5:
        st.subheader("Lista de Estudiantes")
        
        # Mostrar el DataFrame de estudiantes antes de modificar
        st.write("Lista de Estudiantes")
        st.dataframe(df_estudiantes)

# Usar session_state para mantener la ejecución controlada
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    mostrar()
