import streamlit as st
from modulos import db_conector
from modulos.main_Componentes import Componentes_estudiantes  # Asegúrate de que la ruta sea correcta
from modulos import CrearTablas

def mostrar():
    st.header("Módulo de Estudiantes")

    # Obtener la lista de estudiantes y padres
    estudiantes = db_conector.obtener_estudiantes_1()
    padres = db_conector.obtener_padres()  
    estudiantes_dict = {f"{est['nombre_estudiante']} {est['apellido_estudiante']} - Cédula: {est['cedula_estudiante']} (ID: {est['id_estudiante']})": est for est in estudiantes}
    padres_dict = {f"{padre['nombre']} {padre['apellido']} - Cédula: {padre['cedula']} (ID: {padre['id_padres']})": padre['id_padres'] for padre in padres}

    # Crear pestañas
    tab2, tab3, tab4,tab5 = st.tabs(["Agregar Estudiante", "Modificar Estudiante", "Cambiar estado Estudiante","Lista de Estudiantes"])

    # Crear un DataFrame a partir de los estudiantes
    df_estudiantes = CrearTablas.crear_dataframe(estudiantes)
    df_estudiantes = df_estudiantes.rename(columns={
    'id_estudiante': 'ID Estudiante',
    'nombre_estudiante': 'Nombre',
    'apellido_estudiante': 'Apellido',
    'matricula': 'Matrícula',
    'cedula_estudiante': 'Cédula',
    'estado':'Estado',
    'razon':'Razon',
    'genero': 'Género',
    'id_padre': 'ID Padre',
    'nombre_padre': 'Nombre Padre',
    'apellido_padre': 'Apellido Padre',
    'cedula_padre': 'Cédula Padre'
})


        # Pestaña de Agregar Estudiante
    with tab2:
        st.subheader("Agregar Estudiante")
        nombre = st.text_input("Nombre", key="nombre_input")
        apellido = st.text_input("Apellido", key="apellido_input")
        matricula = st.text_input("Matrícula", key="matricula_input")
        cedula = st.text_input("Cédula", key="cedula_input")
        genero = st.selectbox("Género", ["varon", "hembra"], key="genero_input")
        
        padre_seleccionado = st.selectbox("Seleccionar Padre", list(padres_dict.keys()), key="padre_input")
        
        if st.button("Agregar Estudiante"):
            if not matricula:
                st.error("La matrícula no puede estar vacía.")
            else:
                # Aquí puedes hacer una consulta para verificar si la matrícula ya existe en la base de datos
                if db_conector.matricula_existe(matricula):
                    st.error("La matrícula ya existe. Por favor, ingresa una matrícula única.")
                if db_conector.cedula_existe(cedula):
                    st.error("La cedula ya existe. Por favor, ingresa una matrícula única.")
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

        estudiante_seleccionado = st.selectbox("Seleccionar Estudiante para Modificar", list(estudiantes_dict.keys()))
        
        if estudiante_seleccionado:
            est_data = estudiantes_dict[estudiante_seleccionado]
            
            # Asegúrate de que est_data contenga las claves correctas
            nuevo_nombre = st.text_input("Nuevo Nombre", value=est_data['nombre_estudiante'])
            nuevo_apellido = st.text_input("Nuevo Apellido", value=est_data['apellido_estudiante'])
            nueva_matricula = st.text_input("Nueva Matrícula", value=est_data['matricula'])
            nueva_cedula = st.text_input("Nueva Cédula", value=est_data['cedula_estudiante'])

            if st.button("Modificar Estudiante"):
                # Llama a la función modificando la llamada para pasar el diccionario completo
                Componentes_estudiantes.modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula)
                st.success("Estudiante modificado exitosamente")

    # Pestaña de Eliminar Estudiante
    
    with tab4:
        st.subheader("Cambiar Estado de Estudiante")

        # Mostrar el DataFrame de estudiantes antes de cambiar el estado
        st.write("Lista de Estudiantes")
        st.dataframe(df_estudiantes)

        # Cambiar el selectbox a un multiselect
        estudiantes_a_modificar = st.multiselect("Seleccionar Estudiantes", list(estudiantes_dict.keys()))

        # Selector para el nuevo estado
        nuevo_estado = st.selectbox("Nuevo Estado", ["Activo", "Inactivo", "Retirado", "Expulsado", "Graduado"])

        # Campos adicionales para la descripción del cambio
        descripcion = st.text_input("Descripción del Cambio", "Cambio de estado en el sistema.")
        

        if estudiantes_a_modificar and nuevo_estado and descripcion:
            ids_a_modificar = [estudiantes_dict[estudiante]['id_estudiante'] for estudiante in estudiantes_a_modificar]

            # Botón para confirmar el cambio de estado
            if st.button("Cambiar Estado de Estudiantes"):
                for est_id in ids_a_modificar:
                    # Llamada a la función en `Componentes_estudiantes` para cambiar el estado y registrar el cambio
                    Componentes_estudiantes.cambiar_estado_estudiante(est_id, nuevo_estado, descripcion)
                st.success("Estado de estudiantes actualizado correctamente.")
    with tab5:
        st.subheader("Lista de Estudiantes")
        
        # Mostrar el DataFrame de estudiantes antes de modificar
        st.write("Lista de Estudiantes")
        st.dataframe(df_estudiantes)

# Llama a la función para mostrar el módulo
mostrar()
