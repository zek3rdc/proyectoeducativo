import streamlit as st
from modulos import db_conector
from modulos.main_Componentes import Componentes_estudiantes  # Asegúrate de que la ruta sea correcta
from modulos import CrearTablas
import controlador
from modulos.main_Componentes import graficar_torta, grafico_lineal
from modulos.Utilidades.FuncionesGenerales import subHeader
import datetime
import time
import pandas as pd

def dashboard():

    subHeader('Estudiantes', divider='rainbow',)
        # Obtener la lista de estudiantes y padres
    estudiantes = db_conector.obtener_ESTUDIANTES_1()
    

    # Verificar si no hay estudiantes
    if estudiantes is None or len(estudiantes) == 0:
        st.warning("No hay estudiantes en la base de datos.")

    # Crear un DataFrame a partir de los estudiantes
    if estudiantes:
        df_estudiantes = CrearTablas.crear_dataframe(estudiantes)
        df_estudiantes = Componentes_estudiantes.renombrar_columnas(df_estudiantes)
    else:
        df_estudiantes = None


    if df_estudiantes is not None:
              # 2. Gráfico lineal: frecuencia de ingreso comparado al año escolar anterior
            st.subheader("Frecuencia de Ingreso Comparado con el Año Escolar Anterior")
            fig2 = grafico_lineal.crear_grafico_lineal(df_estudiantes)
            # 1. Gráfico de torta: cantidad de niñas y niños
            with st.expander("Distribución de Género"):
                    fig1 = graficar_torta.crear_grafico_torta(df_estudiantes)

            with st.expander("Mostrar/ocultar detalles de los estudiantes"):
                st.dataframe(df_estudiantes)


    else:
        st.warning("No hay estudiantes para mostrar.")


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
    tab2, tab3, tab4, tab5, tab6 = st.tabs(["Agregar Estudiante", "Modificar Estudiante", "Cambiar estado Estudiante", "Asignar Seccion","Lista de Estudiantes"])

    # Crear un DataFrame a partir de los estudiantes
    if estudiantes:
        df_estudiantes = CrearTablas.crear_dataframe(estudiantes)
        df_estudiantes = Componentes_estudiantes.renombrar_columnas(df_estudiantes)
    else:
        df_estudiantes = None

    # Pestaña de Agregar Estudiante
    
    with tab2:
        # Crear formulario
        with st.form("form_agregar_estudiante"):
            nombre_agregar = st.text_input("Nombre")
            apellido_agregar = st.text_input("Apellido")
            cedula_agregar = st.text_input("Cédula")
            cedula_est = st.text_input("Cédula Estudiantil")
            genero_input_agregar = st.selectbox("Género", ["varon", "hembra"])
            estado_agregar = st.selectbox("Estado", ["Activo", "Inactivo"])
            condicion_agregar = st.text_input("Condición especial (opcional)")
            fecha_nac = st.date_input("Fecha de Nacimiento")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")

            # Selección de padre
            padre_seleccionado = st.selectbox(
                "Seleccionar Representante",
                list(padres_dict.keys()),
                index=0
            ) if padres_dict else None

            # Botón para enviar el formulario
            submitted = st.form_submit_button("Agregar Estudiante")

            if submitted:
                # Validar campos requeridos
                errores = []

                if not email.strip():
                    errores.append("El email no puede estar vacío.")
                if not telefono.strip():
                    errores.append("El teléfono no puede estar vacío.")
                if not telefono.isdigit():
                    errores.append("El telefono debe ser numérico.")
                if not fecha_nac:
                    errores.append("La fecha de nacimiento no puede estar vacía.")       
                # Validación de nombre y apellido
                if not nombre_agregar.strip():
                    errores.append("El nombre no puede estar vacío.")
                if not apellido_agregar.strip():
                    errores.append("El apellido no puede estar vacío.")

                # Validación de cédula
                if not cedula_agregar.strip():
                    errores.append("La cédula no puede estar vacía.")
                elif not cedula_agregar.isdigit():
                    errores.append("La cédula debe ser numérica.")
                elif db_conector.cedula_existe(cedula_agregar):
                    errores.append("La cédula ya existe. Por favor, ingresa una cédula única.")

                # Mostrar errores si los hay
                if errores:
                    for error in errores:
                        st.error(error)
                else:
                    # Asignar el ID del representante seleccionado
                    id_representante = padres_dict.get(padre_seleccionado) if padre_seleccionado else None
                    

                    # Insertar estudiante en la base de datos
                    id_nuevo_estudiante = Componentes_estudiantes.agregar_estudiante(
                        nombre=nombre_agregar.strip(),
                        apellido=apellido_agregar.strip(),
                        cedula=int(cedula_agregar.strip()),
                        cedula_est=int(cedula_est.strip()),
                        genero=genero_input_agregar,
                        id_representante=id_representante,
                        estado=estado_agregar,
                        condicion=condicion_agregar.strip() or "N/A",
                        fecha_nac=fecha_nac,
                        email=email.strip(),
                        telefono=int(telefono.strip())
                    )

                    # Mostrar el mensaje de éxito o de error
                    if isinstance(id_nuevo_estudiante, str):  # Si el mensaje de error es una cadena
                        st.error(id_nuevo_estudiante)
                    else:
                        st.success("Estudiante agregado exitosamente.")
                        time.sleep(2)  # Esperar 2 segundos antes de continuar
                        st.rerun()  # Recargar la página para que desaparezca el mensaje
            
        
    # Pestaña de Modificar Estudiante
    with tab3:
        st.subheader("Modificar Estudiante")
        
        if estudiantes_dict:
            # Seleccionar estudiante
            estudiante_seleccionado = st.selectbox(
                "Seleccionar Estudiante para Modificar",
                list(estudiantes_dict.keys()),
            )
            
            # Obtener los datos del estudiante seleccionado
            est_data = estudiantes_dict[estudiante_seleccionado]
            
            # Crear formulario
            with st.form("form_modificar_estudiante"):
                nombre_modificar = st.text_input("Nuevo Nombre", value=est_data['NOMBRE_EST'])
                apellido_modificar = st.text_input("Nuevo Apellido", value=est_data['APELLIDO_EST'])
                cedula_modificar = st.text_input("Nueva Cédula", value=str(est_data['CI_EST']))
                cedula_est_modificar = st.text_input("Nueva Cédula Estudiantil", value=str(est_data['CEDULA_EST']))
                telefono_modificar = st.text_input("Nuevo Teléfono", value=str(est_data['TELEFONO_EST']))
                email_modificar = st.text_input("Nuevo Email", value=est_data['EMAIL_EST'])
                # Normalizar el valor de 'GENERO' a minúsculas antes de buscar en la lista
                genero_modificar = st.selectbox(
                    "Nuevo Género", 
                    ["varon", "hembra"], 
                    index=["varon", "hembra"].index(est_data['GENERO'].lower())
                )

                
                condicion_modificar = st.text_input("Condición Especial (opcional)", value=est_data.get('CONDICION', ''))

                # Botón para enviar el formulario
                submitted = st.form_submit_button("Modificar Estudiante")

                if submitted:
                    # Validar campos requeridos
                    errores = []
                    
                    if not telefono_modificar.strip():
                        errores.append("El teléfono no puede estar vacío.")
                    if not telefono_modificar.isdigit():
                        errores.append("El telefono debe ser numérico.")
                    if not email_modificar.strip():
                        errores.append("El email no puede estar vacío.")

                    # Validación de nombre y apellido
                    if not nombre_modificar.strip():
                        errores.append("El nombre no puede estar vacío.")
                    if not apellido_modificar.strip():
                        errores.append("El apellido no puede estar vacío.")
                    
                    # Validación de cédula
                    if not cedula_modificar.strip():
                        errores.append("La cédula no puede estar vacía.")
                    elif not cedula_modificar.isdigit():
                        errores.append("La cédula debe ser numérica.")
                    elif db_conector.cedula_existe(cedula_modificar) and cedula_modificar != str(est_data['CI_EST']):
                        errores.append("La cédula ya existe. Por favor, ingresa una cédula única.")
                    
                    # Validación de cédula estudiantil
                    if not cedula_est_modificar.strip():
                        errores.append("La cédula estudiantil no puede estar vacía.")
                    elif not cedula_est_modificar.isdigit():
                        errores.append("La cédula estudiantil debe ser numérica.")
                    elif db_conector.matricula_existe(cedula_est_modificar) and cedula_est_modificar != str(est_data['CEDULA_EST']):
                        errores.append("La cédula estudiantil ya existe. Por favor, ingresa una cédula estudiantil única.")

                    # Mostrar errores si los hay
                    if errores:
                        for error in errores:
                            st.error(error)
                    else:
                        # Modificar estudiante en la base de datos
                        exito = Componentes_estudiantes.modificar_estudiante(
                            id_estudiante=est_data['ID_EST'],
                            nuevo_nombre=nombre_modificar.strip(),
                            nuevo_apellido=apellido_modificar.strip(),
                            nueva_cedula=int(cedula_modificar.strip()),
                            nueva_cedula_est=int(cedula_est_modificar.strip()),
                            nuevo_genero=genero_modificar,
                      
                            nueva_condicion=condicion_modificar.strip() or "N/A",
                            nuevo_telefono=int(telefono_modificar.strip()),
                            nuevo_email=email_modificar.strip()
                        )
                        
                        # Mostrar mensaje según el resultado
                        if exito:
                            st.success("Estudiante modificado exitosamente.")
                            time.sleep(2)  # Esperar 2 segundos antes de continuar
                            st.rerun()  # Recargar la página para reflejar los cambios
                        else:
                            st.error("Ocurrió un error al modificar el estudiante. Por favor, verifica los datos e intenta nuevamente.")
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
                st.rerun() 
        else:
            st.warning("Seleccione al menos un estudiante y complete los campos para cambiar el estado.")

    # Pestaña de Lista de Estudiantes
    with tab6:
        st.subheader("Resumen Estudiantes")

        if df_estudiantes is not None:
            # Filtrar estudiantes activos
            df_estudiantes_activos = df_estudiantes[df_estudiantes['Estado'] == 'Activo']

            # 1. Gráfico de torta: cantidad de niñas y niños
            st.subheader("Distribución de Género")
            fig1 = graficar_torta.crear_grafico_torta(df_estudiantes_activos)

            with st.expander("Mostrar/ocultar información de género"):
                # Crear un DataFrame solo con la información de género
                df_genero = df_estudiantes_activos[['Nombre Estudiante', 'Apellido Estudiante', 'Género']]
                st.dataframe(df_genero)

            # 2. Gráfico lineal: frecuencia de ingreso comparado al año escolar anterior
            st.subheader("Frecuencia de Ingreso Comparado con el Año Escolar Anterior")
            fig2 = grafico_lineal.crear_grafico_lineal(df_estudiantes_activos)

            with st.expander("Mostrar/ocultar información de ingreso"):
                # Crear un DataFrame solo con la información de ingreso
                df_frecuencia = df_estudiantes_activos[['Nombre Estudiante', 'Apellido Estudiante', 'Fecha de Registro']]
                st.dataframe(df_frecuencia)

            # 4. Tabla grande con todos los estudiantes activos
            st.subheader("Información Completa de Todos los Estudiantes")
            st.dataframe(df_estudiantes)
        else:
            st.warning("No hay estudiantes para mostrar.")

        # Cargar estudiantes y secciones

        # Mostrar la interfaz en el tab5
    with tab5:
        st.subheader("Asignar, Eliminar o Transferir Estudiantes entre Secciones")
        secciones = db_conector.obtener_secciones()  # Lista de secciones
        df_secciones = pd.DataFrame(secciones, columns=["ID_SECCION", "NOMBRE_SECCION", "GRADO", "PROFESOR"])

        if df_estudiantes is None or df_estudiantes.empty:
            st.warning("No hay estudiantes disponibles en la base de datos.")
        else:
            # Reemplazar valores nulos con "Sin asignar" en la columna 'Sección Asignada'
            df_estudiantes['Sección Asignada'] = df_estudiantes['Sección Asignada'].fillna("Sin asignar")
            estudiantes_sin_seccion = df_estudiantes[df_estudiantes['Sección Asignada'] == "Sin asignar"]
            estudiantes_con_seccion = df_estudiantes[df_estudiantes['Sección Asignada'] != "Sin asignar"]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Estudiantes Sin Sección Asignada")
                st.dataframe(estudiantes_sin_seccion)

            with col2:
                st.subheader("Secciones")
                st.dataframe(df_secciones)

            st.markdown("---")
            st.subheader("Opciones de Gestión de Secciones")

                # Asignar estudiante a una sección
            st.markdown("### Asignar Estudiante a una Sección")
            selected_estudiante = st.multiselect(
                "Selecciona uno o más estudiantes",
                estudiantes_sin_seccion['Nombre Estudiante'] + ' ' + estudiantes_sin_seccion['Apellido Estudiante']
            )
            selected_seccion = st.selectbox(
                "Selecciona una sección",
                options=df_secciones['NOMBRE_SECCION'],
                key="asignar_seccion"
            )

            if st.button("Asignar Sección"):
                if selected_estudiante:
                    # Crear la columna 'Nombre Completo' para facilitar la comparación
                    estudiantes_sin_seccion['Nombre Completo'] = (
                        estudiantes_sin_seccion['Nombre Estudiante'] + ' ' + estudiantes_sin_seccion['Apellido Estudiante']
                    )

                    # Filtrar los estudiantes seleccionados
                    estudiantes_filtrados = estudiantes_sin_seccion[
                        estudiantes_sin_seccion['Nombre Completo'].isin(selected_estudiante)
                    ]

                    if not estudiantes_filtrados.empty:
                        # Obtener el ID de la sección seleccionada
                        id_seccion = df_secciones[df_secciones['NOMBRE_SECCION'] == selected_seccion]['ID_SECCION'].iloc[0]

                        # Iterar sobre los estudiantes seleccionados
                        for _, estudiante in estudiantes_filtrados.iterrows():
                            id_estudiante = int(estudiante['ID Estudiante'])

                            # Intentar asignar el estudiante a la sección
                            resultado = db_conector.asignar_estudiante_a_seccion(id_estudiante, id_seccion)

                            if resultado:
                                st.success(f"Sección '{selected_seccion}' asignada exitosamente al estudiante '{estudiante['Nombre Completo']}'.")
                            else:
                                st.error(f"El estudiante '{estudiante['Nombre Completo']}' ya está asignado a la sección '{selected_seccion}'.")
                        
                        # Rehacer la carga de la página después de la acción
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.warning("No se encontraron estudiantes seleccionados.")
                else:
                    st.warning("Selecciona al menos un estudiante para asignar.")

            # Eliminar estudiante de una sección
            st.markdown("### Eliminar Estudiante de una Sección")
            selected_estudiante_con_seccion = st.multiselect(
                "Selecciona un estudiante con sección asignada",
                estudiantes_con_seccion['Nombre Estudiante'] + ' ' + estudiantes_con_seccion['Apellido Estudiante'],
                key="eliminar_estudiante"
            )

            if st.button("Eliminar Estudiante de la Sección"):
                if selected_estudiante_con_seccion:
                    # Crear la columna 'Nombre Completo' para facilitar la comparación
                    estudiantes_con_seccion['Nombre Completo'] = (
                        estudiantes_con_seccion['Nombre Estudiante'] + ' ' + estudiantes_con_seccion['Apellido Estudiante']
                    )

                    # Filtrar los estudiantes seleccionados
                    estudiantes_filtrados = estudiantes_con_seccion[
                        estudiantes_con_seccion['Nombre Completo'].isin(selected_estudiante_con_seccion)
                    ]

                    if not estudiantes_filtrados.empty:
                        # Iterar sobre los estudiantes seleccionados
                        for _, estudiante in estudiantes_filtrados.iterrows():
                            id_estudiante = int(estudiante['ID Estudiante'])

                            # Intentar eliminar al estudiante de la sección
                            resultado = db_conector.eliminar_estudiante_de_seccion(id_estudiante)

                            if resultado:
                                st.success(f"Estudiante '{estudiante['Nombre Completo']}' eliminado de su sección.")
                            else:
                                st.error(f"No se pudo eliminar al estudiante '{estudiante['Nombre Completo']}' de su sección.")
                        
                        # Rehacer la carga de la página después de la acción
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.warning("No se encontraron estudiantes seleccionados.")
                else:
                    st.warning("Selecciona al menos un estudiante para eliminar.")


            # Transferir estudiante a otra sección
            st.markdown("### Transferir Estudiante a Otra Sección")
            selected_estudiante_con_seccion = st.multiselect(
                "Selecciona un estudiante con sección asignada",
                estudiantes_con_seccion['Nombre Estudiante'] + ' ' + estudiantes_con_seccion['Apellido Estudiante'],
                key="transferir_estudiante"
            )
            selected_seccion_nueva = st.selectbox(
                "Selecciona una nueva sección",
                options=df_secciones['NOMBRE_SECCION'],
                key="transferir_seccion"
            )

            if st.button("Transferir Estudiante"):
                if selected_estudiante_con_seccion:
                    # Crear la columna 'Nombre Completo' para facilitar la comparación
                    estudiantes_con_seccion['Nombre Completo'] = (
                        estudiantes_con_seccion['Nombre Estudiante'] + ' ' + estudiantes_con_seccion['Apellido Estudiante']
                    )

                    # Filtrar el estudiante seleccionado
                    estudiante_seleccionado = estudiantes_con_seccion[
                        estudiantes_con_seccion['Nombre Completo'].isin(selected_estudiante_con_seccion)
                    ].iloc[0]

                    id_estudiante = int(estudiante_seleccionado['ID Estudiante'])
                    id_seccion_nueva = df_secciones[df_secciones['NOMBRE_SECCION'] == selected_seccion_nueva]['ID_SECCION'].iloc[0]

                    # Intentar eliminar al estudiante de la sección actual
                    resultado_eliminacion = db_conector.eliminar_estudiante_de_seccion(id_estudiante)
                    
                    if resultado_eliminacion:
                        # Si la eliminación fue exitosa, proceder con la asignación a la nueva sección
                        resultado_asignacion = db_conector.asignar_estudiante_a_seccion(id_estudiante, id_seccion_nueva)

                        if resultado_asignacion:
                            st.success(f"Estudiante '{estudiante_seleccionado['Nombre Completo']}' transferido exitosamente a la sección '{selected_seccion_nueva}'.")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"No se pudo asignar al estudiante '{estudiante_seleccionado['Nombre Completo']}' a la sección '{selected_seccion_nueva}'.")
                    else:
                        st.error(f"No se pudo eliminar al estudiante '{estudiante_seleccionado['Nombre Completo']}' de su sección actual.")
                else:
                    st.warning("Selecciona un estudiante para transferir.")

            # Expander para mostrar datos adicionales
            with st.expander("Ver datos adicionales"):
                st.markdown("#### Secciones Disponibles")
                st.dataframe(df_secciones)

                st.markdown("#### Estudiantes con Sección Asignada")
                st.dataframe(estudiantes_con_seccion)
