import plotly.graph_objects as go
import streamlit as st
import os

def crear_grafico_torta(df_estudiantes):
    """
    Crea un gráfico de torta interactivo mostrando la distribución de género de los estudiantes
    y lo guarda como imagen en una ruta específica.
    """
    try:
        # Verifica que la columna 'Género' exista
        if 'Género' not in df_estudiantes.columns:
            raise ValueError("La columna 'Género' no se encuentra en el DataFrame")

        # Contar valores de la columna 'Género'
        genero_count = df_estudiantes['Género'].value_counts()
        
        # Colores personalizados para el gráfico de torta
        colores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
        
        # Crear el gráfico de torta interactivo
        fig = go.Figure(data=[go.Pie(
            labels=genero_count.index, 
            values=genero_count, 
            hoverinfo='label+percent',  # Información de hover
            textinfo='label+percent',   # Información dentro del gráfico
            marker=dict(colors=colores),
            pull=[0.1] * len(genero_count),  # Efecto de explosión para cada segmento
            textfont=dict(size=14, color='black')  # Fuente del texto dentro del gráfico
        )])
        
        # Personalización adicional del gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>%{percent:.2f}%<br>'  # Formato de hover
        )
        
        # Actualizar el layout para mejor presentación
        fig.update_layout(
            showlegend=True,
            title_text="Distribución de Género de los Estudiantes",
            title_x=0.5,  # Centrado del título
            title_font_size=16,
            margin=dict(t=40, b=40, l=40, r=40)
        )
        
        # Guardar la imagen en la ruta especificada
        output_dir = r"C:\Users\jozek\Documents\tareas\ProyectoSCM\S.comunitario\UENB\dependencias\grafico_torta"
        output_path = os.path.join(output_dir, "grafico_torta.png")
        
        # Crear el directorio si no existe
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                st.error(f"Error al crear el directorio para guardar el gráfico: {e}")
                return None
        
        # Guardar la figura como imagen usando Plotly
        try:
            fig.write_image(output_path, engine="kaleido")  # Método correcto de Plotly
           
        except Exception as e:
            st.warning(f"Advertencia: No se pudo guardar el gráfico. Detalle: {e}")
        
        # Mostrar el gráfico en Streamlit (sin 'key' para evitar duplicados)
        try:
            st.plotly_chart(fig, use_container_width=True)  # Mostrar el gráfico con ajuste de ancho
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
