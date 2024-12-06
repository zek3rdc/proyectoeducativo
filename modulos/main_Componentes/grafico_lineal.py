# graficolineal.py
import matplotlib.pyplot as plt
import pandas as pd

def crear_grafico_lineal(df_estudiantes):
    """
    Crea un gráfico lineal mostrando la frecuencia de ingreso comparada con el año escolar anterior.
    """
    # Convertir la columna 'ingreso' a tipo datetime para extraer el año de ingreso
    df_estudiantes['año_ingreso'] = pd.to_datetime(df_estudiantes['ingreso']).dt.year
    
    # Agrupar por año de ingreso y contar la cantidad de estudiantes por año
    ingreso_frecuencia = df_estudiantes.groupby('año_ingreso').size()
    
    # Crear el gráfico lineal
    fig2, ax2 = plt.subplots()
    ax2.plot(ingreso_frecuencia.index, ingreso_frecuencia.values, marker='o', linestyle='-', color='b')
    ax2.set_title('Frecuencia de Ingreso por Año Escolar')
    ax2.set_xlabel('Año Escolar')
    ax2.set_ylabel('Cantidad de Estudiantes')
    
    return fig2
