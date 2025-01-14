import streamlit as st
from modulos.main_Componentes import componente_grados
from modulos import db_conector
import pandas as pd

def mostrar():
    """
    Muestra el módulo de gestión de grados en la interfaz de usuario.
    """
    st.header("Gestión de Grados")
    st.write("Aquí puedes agregar, modificar, eliminar grados, asignarlos a secciones o quitar asignaciones.")

    # Obtener lista de grados y secciones
    grados = componente_grados.obtener_grados()
    secciones = db_conector.obtener_secciones()

    # Convertir datos a DataFrames para visualización
    df_grados = pd.DataFrame(grados, columns=["ID_GRADO", "NOMBRE_GRADO"])
    df_secciones = pd.DataFrame(secciones, columns=["ID_SECCION", "NOMBRE_SECCION", "ID_GRADO", "NOMBRE_GRADO"])

    # Mostrar los datos actuales
    st.write("Lista de Grados:")
    st.dataframe(df_grados, use_container_width=True)

    # Agregar un nuevo grado
    with st.expander("Agregar Grado"):
        nombre_grado = st.text_input("Nombre del nuevo grado")
        if st.button("Agregar Grado"):
            if componente_grados.agregar_grado(nombre_grado):
                st.success("Grado agregado exitosamente.")
                st.rerun()

    # Modificar un grado existente
    with st.expander("Modificar Grado"):
        if not df_grados.empty:
            grado_seleccionado = st.selectbox(
                "Selecciona un grado para modificar",
                df_grados.values.tolist(),
                format_func=lambda x: f"{x[0]} - {x[1]}" if isinstance(x, (list, tuple)) else str(x)
            )

            nuevo_nombre = st.text_input("Nuevo nombre del grado", value=grado_seleccionado[1])
            if st.button("Modificar Grado"):
                if componente_grados.modificar_grado(grado_seleccionado[0], nuevo_nombre):
                    st.success("Grado modificado exitosamente.")
                    st.rerun()
        else:
            st.info("No hay grados registrados.")

    # Eliminar grados (Multiselección)
    with st.expander("Eliminar Grado"):
        if not df_grados.empty:
            grados_a_eliminar = st.multiselect(
                "Selecciona los grados para eliminar",
                df_grados.values.tolist(),
                format_func=lambda x: f"{x[0]} - {x[1]}" if isinstance(x, (list, tuple)) else str(x)
            )

            if st.button("Eliminar Grado(s)"):
                for grado in grados_a_eliminar:
                    if componente_grados.eliminar_grado(grado[0]):
                        st.success(f"Grado {grado[1]} eliminado exitosamente.")
                st.rerun()
        else:
            st.info("No hay grados registrados.")

    # Asignar o quitar grado a sección (Multiselección)
    with st.expander("Asignar o Quitar Grado a Sección"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Grados")
            st.dataframe(df_grados, use_container_width=True)

        with col2:
            st.subheader("Secciones")
            filtro = st.radio("Filtrar secciones por:", ["Todas", "Con Grado", "Sin Grado"], index=0)
            if filtro == "Con Grado":
                df_secciones_filtradas = df_secciones[df_secciones["ID_GRADO"].notna()]
            elif filtro == "Sin Grado":
                df_secciones_filtradas = df_secciones[df_secciones["ID_GRADO"].isna()]
            else:
                df_secciones_filtradas = df_secciones

            st.dataframe(df_secciones_filtradas, use_container_width=True)

        grados_seleccionados = st.multiselect(
            "Selecciona los grados",
            df_grados.values.tolist(),
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )

        secciones_seleccionadas = st.multiselect(
            "Selecciona las secciones",
            df_secciones.values.tolist(),
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )

        col3, col4 = st.columns(2)
        with col3:
            if st.button("Asignar Grado(s) a Sección(es)"):
                for grado in grados_seleccionados:
                    for seccion in secciones_seleccionadas:
                        if componente_grados.asignar_grado_a_seccion(grado[0], seccion[0]):
                            st.success(f"Grado {grado[1]} asignado exitosamente a la sección {seccion[1]}.")
                st.rerun()
        with col4:
            if st.button("Quitar Grado(s) de Sección(es)"):
                for seccion in secciones_seleccionadas:
                    if componente_grados.quitar_grado_de_seccion(seccion[0]):
                        st.success(f"Grado quitado exitosamente de la sección {seccion[1]}.")
                st.rerun()

    # Mostrar grados y secciones
    with st.expander("Ver Grados y Secciones"):
        st.subheader("Grados")
        st.dataframe(df_grados, use_container_width=True)

        st.subheader("Secciones")
        st.dataframe(df_secciones, use_container_width=True)
