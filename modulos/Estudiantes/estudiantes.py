import streamlit as st
from modulos import db_conector
from modulos.main_Componentes import Componentes_estudiantes  # Asegúrate de que la ruta sea correcta
from modulos import CrearTablas
import controlador
from modulos.main_Componentes import graficar_torta, grafico_lineal

def mostrar():
    st.header("Módulo de Estudiantes")
    
    # Obtener la lista de estudiantes y padres
    estudiantes = db_conector.obtener_ESTUDIANTES_1()
    padres = db_conector.obtener_padres()  

    # Verificar si no hay estudiantes
    if estudiantes is None or len(estudiantes) == 0:
        st.warning("No hay estudiantes en la base de datos.")
        estudiantes_dict = {}
    else:
        estudiantes_dict = {
            f"{est['NOMBRE_EST']} {est['APELLIDO_EST']} - Cédula Estudiantil: {est['CEDULA_EST']} (ID: {est['ID_EST']})": est
            for est in estudiantes
        }

    # Verificar si no hay padres
    if padres is None or len(padres) == 0:
        st.warning("No hay padres en la base de datos.")
        padres_dict = {}
    else:
        padres_dict = {f"{padre['NOMBRE_REP']} {padre['APELLIDO_REP']} - Cédula: {padre['CEDULA_REP']} (ID: {padre['ID_REP']})": padre['ID_REP'] for padre in padres}

    # Crear pestañas
    tab2, tab3, tab4, tab5 = st.tabs(["Agregar Estudiante", "Modificar Estudiante", "Cambiar estado Estudiante", "Lista de Estudiantes"])

    # Crear un DataFrame a partir de los estudiantes
    if estudiantes:
        df_estudiantes = CrearTablas.crear_dataframe(estudiantes)
        df_estudiantes = Componentes_estudiantes.renombrar_columnas(df_estudiantes)
    else:
        df_estudiantes = None

    # Pestaña de Agregar Estudiante
    with tab2:
        # Inicializar valores en session_state si no existen
        if "nombre_agregar" not in st.session_state:
            st.session_state.nombre_agregar = ""
        if "apellido_agregar" not in st.session_state:
            st.session_state.apellido_agregar = ""
        if "matricula_agregar" not in st.session_state:
            st.session_state.matricula_agregar = ""
        if "cedula_agregar" not in st.session_state:
            st.session_state.cedula_agregar = ""
        if "genero_input_agregar" not in st.session_state:
            st.session_state.genero_input_agregar = "varon"

        # Crear formulario
        with st.form("form_agregar_estudiante"):
            st.text_input("Nombre", key="nombre_agregar")
            st.text_input("Apellido", key="apellido_agregar")
            st.text_input("Matrícula", key="matricula_agregar")
            st.text_input("Cédula", key="cedula_agregar")
            st.selectbox("Género", ["varon", "hembra"], key="genero_input_agregar")
            
            padre_seleccionado = None
            if padres_dict:
                padre_seleccionado = st.selectbox("Seleccionar Padre", list(padres_dict.keys()))

            # Botón dentro del formulario
            submitted = st.form_submit_button("Agregar Estudiante")

            if submitted:
                if not st.session_state.matricula_agregar:
                    st.error("La matrícula no puede estar vacía.")
                elif db_conector.matricula_existe(st.session_state.matricula_agregar):
                    st.error("La cédula estudiantil ya existe. Por favor, ingresa una cédula estudiantil única.")
                elif db_conector.cedula_existe(st.session_state.cedula_agregar):
                    st.error("La cédula ya existe. Por favor, ingresa una cédula única.")
                else:
                    id_padre = padres_dict.get(padre_seleccionado) if padre_seleccionado else None
                    if id_padre:
                        id_nuevo_estudiante = Componentes_estudiantes.agregar_estudiante(
                            st.session_state.nombre_agregar,
                            st.session_state.apellido_agregar,
                            st.session_state.matricula_agregar,
                            st.session_state.cedula_agregar,
                            id_padre,
                            st.session_state.genero_input_agregar
                        )
                        st.success("Estudiante agregado y vinculado al padre exitosamente.")
                    
        
    # Pestaña de Modificar Estudiante
    with tab3:
        st.subheader("Modificar Estudiante")
        
        # Mostrar el DataFrame de estudiantes antes de modificar
        if df_estudiantes is not None:
            st.write("Lista de Estudiantes")
            st.dataframe(df_estudiantes)

        if estudiantes_dict:
            # Almacenar el estudiante seleccionado en session_state
            if "estudiante_seleccionado" not in st.session_state:
                st.session_state["estudiante_seleccionado"] = list(estudiantes_dict.keys())[0]  # Primer estudiante por defecto

            # Selección del estudiante para modificar
            estudiante_seleccionado = st.selectbox("Seleccionar Estudiante para Modificar", list(estudiantes_dict.keys()), key="select_estudiante_modificar", index=list(estudiantes_dict.keys()).index(st.session_state["estudiante_seleccionado"]))
            
            # Actualizar el estudiante seleccionado en session_state
            st.session_state["estudiante_seleccionado"] = estudiante_seleccionado
            
            if estudiante_seleccionado:
                est_data = estudiantes_dict[estudiante_seleccionado]
                
                # Crear formulario para modificar el estudiante
                with st.form(key="form_modificar_estudiante"):
                    # Asegúrate de que est_data contenga las claves correctas
                    nuevo_nombre = st.text_input("Nuevo Nombre", value=est_data['nombre_est'], key="nuevo_nombre_input_modificar")
                    nuevo_apellido = st.text_input("Nuevo Apellido", value=est_data['apellido_est'], key="nuevo_apellido_input_modificar")
                    nueva_matricula = st.text_input("Nueva Matrícula", value=est_data['ci_est'], key="nueva_matricula_input_modificar")
                    nueva_cedula = st.text_input("Nueva Cédula", value=est_data['cedula_est'], key="nueva_cedula_input_modificar")

                    # Botón de envío dentro del formulario
                    submitted = st.form_submit_button("Modificar Estudiante")

                    if submitted:
                        # Llama a la función modificando la llamada para pasar el diccionario completo
                        Componentes_estudiantes.modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula)
                        st.success("Estudiante modificado exitosamente")
        else:
            st.warning("No hay estudiantes para modificar.")


    # Pestaña de Cambiar Estado de Estudiante
    with tab4:
        st.subheader("Cambiar Estado de Estudiante")

        # Mostrar el DataFrame de estudiantes antes de cambiar el estado
        if df_estudiantes is not None:
            st.write("Lista de Estudiantes")
            st.dataframe(df_estudiantes)

        # Cambiar el selectbox a un multiselect
        estudiantes_a_modificar = st.multiselect("Seleccionar Estudiantes", list(estudiantes_dict.keys()), key="estudiantes_a_modificar")

        # Selector para el nuevo estado
        nuevo_estado = st.selectbox("Nuevo Estado", ["Activo", "Inactivo", "Retirado", "Expulsado", "Graduado"], key="nuevo_estado_input")

        # Campos adicionales para la descripción del cambio
        descripcion = st.text_input("Descripción del Cambio", "Cambio de estado en el sistema.", key="descripcion_input")
        
        if estudiantes_a_modificar and nuevo_estado and descripcion:
            ids_a_modificar = [estudiantes_dict[estudiante]['ID_EST'] for estudiante in estudiantes_a_modificar]

            # Botón para confirmar el cambio de estado
            if st.button("Cambiar Estado de Estudiantes", key="cambiar_estado_input"):
                for est_id in ids_a_modificar:
                    # Llamada a la función en `Componentes_estudiantes` para cambiar el estado y registrar el cambio
                    Componentes_estudiantes.cambiar_estado_estudiante(est_id, nuevo_estado, descripcion)
                st.success("Estado de estudiantes actualizado correctamente.")
        else:
            st.warning("Seleccione al menos un estudiante y complete los campos para cambiar el estado.")

    # Pestaña de Lista de Estudiantes
    with tab5:
        st.subheader("Resumen Estudiantes")
        
        if df_estudiantes is not None:
            # Mostrar la lista de estudiantes
            st.write("Lista de Estudiantes")
            st.dataframe(df_estudiantes)

            # 1. Gráfico de torta: cantidad de niñas y niños
            st.subheader("Distribución de Género")
            fig1 = graficar_torta.crear_grafico_torta(df_estudiantes)
            

            # 2. Gráfico lineal: frecuencia de ingreso comparado al año escolar anterior
            st.subheader("Frecuencia de Ingreso Comparado con el Año Escolar Anterior")
            fig2 = grafico_lineal.crear_grafico_lineal(df_estudiantes)
            st.pyplot(fig2)

            # 3. Tabla desplegable para ver más detalles de los estudiantes
            st.subheader("Ver Estudiantes Detalladamente")
            st.dataframe(df_estudiantes)

            # 4. Tabla grande con todos los estudiantes
            st.subheader("Información Completa de Todos los Estudiantes")
            st.dataframe(df_estudiantes)
        else:
            st.warning("No hay estudiantes para mostrar.")
# Usar session_state para mantener la ejecución controlada
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    mostrar()
