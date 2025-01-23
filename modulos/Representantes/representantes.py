import streamlit as st
from modulos.Utilidades.FuncionesGenerales import subHeader
from modulos.main_Componentes import componentes_representantes
import pandas as pd
import time
def mostrar():
    st.header("Módulo de Representantes")
    st.write("Gestiona la información de los representantes.")

    # Pestañas para las diferentes secciones
    tabs = st.tabs(["Lista de Representantes", "Agregar Representante", "Editar Representante", "Eliminar Representante"])

    # --- Tab 1: Lista de Representantes ---
    with tabs[0]:
        st.subheader("Lista de Representantes")
        representantes = componentes_representantes.obtener_representantes()

        if representantes is None:
            st.error("Error al obtener la lista de representantes.")
        elif len(representantes) == 0:
            st.info("No hay representantes registrados.")
        else:
            # Convertir los datos a un DataFrame
            df_representantes = pd.DataFrame(representantes)
            
            # Obtener los números de teléfono asociados
            # Obtener los números de teléfono asociados
            for rep in df_representantes["ID_REP"]:
                telefonos = componentes_representantes.obtener_telefonos_representante(rep)
                # Asegúrate de que todos los números sean cadenas antes de unirlos
                df_representantes.loc[df_representantes["ID_REP"] == rep, "TELEFONOS"] = ", ".join(str(tel) for tel in telefonos)

            
            # Mostrar DataFrame en Streamlit
            df_representantes = df_representantes.rename(columns={"ID_REP": "ID","NOMBRE_REP": "Nombre", "APELLIDO_REP": "Apellido", "CEDULA_REP": "Cedula", 
                                                                  "DIRECCION_REP": "Dirección", "TELEFONO_REP": "Teléfono Principal", 
                                                                  "TELEFONOS": "Teléfonos Adicionales","FECHA_NAC_REP":"Fecha de Nacimiento",
                                                                  "FECHA_REG_REP":"Fecha de Registro"})
            st.dataframe(df_representantes)

    # --- Tab 2: Agregar Representante ---
    with tabs[1]:
        st.subheader("Agregar Representante")
        with st.form(key="form_agregar"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            cedula = st.text_input("Cédula")
            direccion = st.text_area("Dirección")
            fecha_nac = st.date_input("Fecha de Nacimiento")
            telefono_principal = st.text_input("Teléfono Principal")
            telefonos_adicionales = st.text_area("Teléfonos Adicionales (separados por comas)")
            submit = st.form_submit_button("Agregar")
            
            if submit:
                # Llamar a la función para agregar el representante y sus teléfonos
                resultado = componentes_representantes.agregar_representante(
                    nombre, apellido, cedula, telefono_principal, direccion, fecha_nac, telefonos_adicionales
                )
                
                if "ID_REP" in resultado:
                    st.success(f"Representante agregado exitosamente con ID: {resultado['ID_REP']}")
                    time.sleep(2) 
                    st.rerun()
                else:
                    st.error(f"Error: {resultado.get('error', 'Ocurrió un error inesperado.')}")


    # --- Tab 3: Editar Representante ---
    with tabs[2]:
        st.subheader("Editar Representante")
        id_editar = st.text_input("ID del Representante a Editar")
        if id_editar:
            with st.form(key="form_editar"):
                nombre = st.text_input("Nuevo Nombre")
                apellido = st.text_input("Nuevo Apellido")
                cedula = st.text_input("Nueva Cédula")
                direccion = st.text_area("Nueva Dirección")
                telefono_principal_edit = st.text_input("Nuevo Teléfono Principal")
                telefonos = st.text_area("Nuevos Teléfonos (separados por comas)")
                submit_editar = st.form_submit_button("Actualizar")
                if submit_editar:
                    if componentes_representantes.actualizar_representante(
                        id_editar, nombre, apellido, cedula, telefono_principal_edit, direccion  # Asegúrate de pasar todos los parámetros
                    ):
                        # Actualizar teléfonos
                        componentes_representantes.eliminar_telefonos_representante(id_editar)  # Eliminar teléfonos anteriores
                        for tel in telefonos.split(","):
                            tel = tel.strip()
                            if tel:
                                componentes_representantes.agregar_telefono(id_editar, tel)
                        time.sleep(2) 
                        st.rerun()
                        st.success("Representante actualizado exitosamente.")
                    else:
                        st.error("Error al actualizar representante.")


    # --- Tab 4: Eliminar Representante ---
    with tabs[3]:
        st.subheader("Eliminar Representante")
        id_eliminar = st.text_input("ID del Representante a Eliminar")
        if st.button("Eliminar"):
            if componentes_representantes.eliminar_representante(id_eliminar):
                st.success("Representante eliminado exitosamente.")
            else:
                st.error("Error al eliminar representante.")
