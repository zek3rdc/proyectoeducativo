import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import os

def crear_grafico_lineal(df_estudiantes):
    """
    Crea un gráfico lineal interactivo mostrando la frecuencia de ingreso por año escolar.
    Guarda el gráfico como imagen en una ruta específica.
    """
    try:
        # Filtrar los estudiantes activos
        df_estudiantes_activos = df_estudiantes[df_estudiantes['Estado'] == 'Activo']

        # Verificar la columna 'Fecha de Registro'
        if 'Fecha de Registro' not in df_estudiantes_activos.columns:
            raise ValueError("La columna 'Fecha de Registro' no existe en el DataFrame.")

        # Convertir la columna 'Fecha de Registro' a tipo datetime si no lo está
        if not pd.api.types.is_datetime64_any_dtype(df_estudiantes_activos['Fecha de Registro']):
            df_estudiantes_activos['Fecha de Registro'] = pd.to_datetime(df_estudiantes_activos['Fecha de Registro'])

        # Extraer el año de la columna 'Fecha de Registro'
        df_estudiantes_activos['Año de Registro'] = df_estudiantes_activos['Fecha de Registro'].dt.year


        # Agrupar por año y contar la cantidad de estudiantes
        ingreso_frecuencia = df_estudiantes_activos.groupby('Año de Registro').size()

        # Crear el gráfico lineal interactivo
        fig = go.Figure(data=[go.Scatter(
            x=ingreso_frecuencia.index,
            y=ingreso_frecuencia.values,
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(size=8),
            name="Frecuencia de Ingreso"
        )])

        # Personalización del gráfico
        fig.update_layout(
            title="Frecuencia de Ingreso por Año Escolar",
            xaxis_title="Año Escolar",
            yaxis_title="Cantidad de Estudiantes",
            title_x=0.5,
            title_font_size=16,
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            margin=dict(t=40, b=40, l=40, r=40),
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo del gráfico transparente
            paper_bgcolor='rgba(0,0,0,0)'  # Fondo del área completa transparente
        )

        # Guardar la imagen en la ruta especificada
        output_dir = r"C:\Users\jozek\Documents\tareas\ProyectoSCM\S.comunitario\UENB\dependencias\grafico_lineal"
        output_path = os.path.join(output_dir, "grafico_lineal.png")

        # Crear el directorio si no existe
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                st.error(f"Error al crear el directorio para guardar el gráfico: {e}")
                return None

        # Guardar la figura como imagen usando Plotly
        try:
            fig.write_image(output_path, engine="kaleido")
        except Exception as e:
            st.warning(f"Advertencia: No se pudo guardar el gráfico. Detalle: {e}")

        # Mostrar el gráfico en Streamlit
        try:
            st.plotly_chart(fig, use_container_width=True, key="grafico_lineal")
        except Exception as e:
            st.error(f"Error al renderizar el gráfico en Streamlit: {e}")
            return None

        return fig

    except ValueError as ve:
        st.error(f"Error en los datos: {ve}")
        return None
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado: {e}")
        return None



def crear_grafico_lineal_secciones(data, x_col, y_col):
    """
    Crea un gráfico lineal interactivo.

    Args:
        data (list): Datos a graficar.
        x_col (str): Nombre de la columna para el eje X.
        y_col (str): Nombre de la columna para el eje Y.
    """
    if not data:
        st.write("No hay datos disponibles para graficar.")
        return

    # Convertir datos a DataFrame
    df = pd.DataFrame(data)
    if x_col not in df.columns or y_col not in df.columns:
        st.write("Las columnas especificadas no existen en los datos.")
        return

    # Crear gráfico lineal
    fig = go.Figure(data=[go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    )])

    # Configuración del gráfico
    fig.update_layout(
        title="Gráfico Lineal",
        xaxis_title=x_col,
        yaxis_title=y_col,
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
