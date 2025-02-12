import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from modulos import db_conector

def crear_grafico_lineal(df_estudiantes):
    """
    Crea un gráfico lineal interactivo mostrando la cantidad de estudiantes por mes, agrupados por estado (ingresos, suben, egresos, etc.).
    Guarda el gráfico como imagen en una ruta específica.
    """
    try:
        # Verificar si las columnas necesarias existen
        if 'Fecha de Registro' not in df_estudiantes.columns or 'Estado' not in df_estudiantes.columns:
            raise ValueError("Las columnas necesarias 'Fecha de Registro' o 'Estado' no existen en el DataFrame.")
        
        # Convertir la columna 'Fecha de Registro' a tipo datetime si no lo está
        if not pd.api.types.is_datetime64_any_dtype(df_estudiantes['Fecha de Registro']):
            df_estudiantes['Fecha de Registro'] = pd.to_datetime(df_estudiantes['Fecha de Registro'])
        
        # Extraer el mes y el año de la columna 'Fecha de Registro'
        df_estudiantes['Mes de Registro'] = df_estudiantes['Fecha de Registro'].dt.to_period('M')

        # Agrupar por mes y estado, contando la cantidad de estudiantes
        estado_mes_frecuencia = df_estudiantes.groupby(['Mes de Registro', 'Estado']).size().unstack(fill_value=0)

        # Crear el gráfico lineal interactivo
        fig = go.Figure()

        # Añadir una línea para cada estado
        for estado in estado_mes_frecuencia.columns:
            fig.add_trace(go.Scatter(
                x=estado_mes_frecuencia.index.astype(str),  # Convertir el Periodo a cadena
                y=estado_mes_frecuencia[estado],
                mode='lines+markers',
                name=estado,
                line=dict(width=2),
                marker=dict(size=8)
            ))

        # Personalización del gráfico
        fig.update_layout(
            title="Estudiantes por Mes y Estado (Ingreso, Suben, Egreso, Retiro, etc.)",
            xaxis_title="Mes",
            yaxis_title="Cantidad de Estudiantes",
            title_x=0.5,
            title_font_size=16,
            xaxis=dict(showgrid=True, gridcolor='lightgray', tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='lightgray'),
            margin=dict(t=40, b=60, l=40, r=40),
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo del gráfico transparente
            paper_bgcolor='rgba(0,0,0,0)'  # Fondo del área completa transparente
        )

        # Guardar la imagen en la ruta especificada
        output_dir = r"C:\Users\jozek\Documents\tareas\ProyectoSCM\S.comunitario\UENB\dependencias\grafico_lineal"
        output_path = os.path.join(output_dir, "grafico_estudiantes_por_mes.png")

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



def crear_grafico_ingreso(df_estudiantes):
    """Genera un gráfico de ingresos comparado con el año escolar anterior."""
    df_estudiantes['Fecha de Registro'] = pd.to_datetime(df_estudiantes['Fecha de Registro'])
    df_estudiantes['Mes-Año'] = df_estudiantes['Fecha de Registro'].dt.to_period('M')

    ingreso_frecuencia = df_estudiantes.groupby('Mes-Año').size()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ingreso_frecuencia.index.astype(str),
        y=ingreso_frecuencia.values,
        mode='lines+markers',
        line=dict(color='yellow', width=2),
        marker=dict(size=8),
        name="Ingresos"
    ))

    fig.update_layout(
        title="Frecuencia de Ingresos por Mes",
        xaxis_title="Mes-Año",
        yaxis_title="Cantidad de Estudiantes",
        title_x=0.5,
        title_font_size=16,
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)


def crear_grafico_asistencias(df_asistencias, df_asistencias_anterior):
    """Genera un gráfico comparando asistencias de la semana actual vs. la anterior."""

    df_asistencias['FECHA_ASISTENCIA'] = pd.to_datetime(df_asistencias['FECHA_ASISTENCIA'], errors='coerce')
    df_asistencias_anterior['FECHA_ASISTENCIA'] = pd.to_datetime(df_asistencias_anterior['FECHA_ASISTENCIA'], errors='coerce')
    def contar_asistencias_por_dia(df):
        df['DIA_SEMANA'] = df['FECHA_ASISTENCIA'].dt.day_name()
        return df.groupby('DIA_SEMANA').size()

    dias_ordenados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    asistencias_actual = contar_asistencias_por_dia(df_asistencias).reindex(dias_ordenados, fill_value=0)
    asistencias_anterior = contar_asistencias_por_dia(df_asistencias_anterior).reindex(dias_ordenados, fill_value=0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dias_ordenados, 
        y=asistencias_anterior.values,
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(size=8),
        name="Semana Anterior"
    ))

    fig.add_trace(go.Scatter(
        x=dias_ordenados, 
        y=asistencias_actual.values,
        mode='lines+markers',
        line=dict(color='yellow', width=2),
        marker=dict(size=8),
        name="Semana Actual"
    ))

    fig.update_layout(
        title="Comparación de Asistencias: Semana Actual vs. Anterior",
        xaxis_title="Día de la Semana",
        yaxis_title="Cantidad de Asistencias",
        title_x=0.5,
        title_font_size=16,
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)