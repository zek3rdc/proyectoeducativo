import pandas as pd
import streamlit as st

# Función para crear un DataFrame a partir de una lista de diccionarios
def crear_dataframe(data, columnas=None):
    # Convertir la lista de diccionarios a DataFrame
    df = pd.DataFrame(data)
    
    # Si se proporcionan nombres de columnas, renombrar
    if columnas:
        df.columns = columnas
    
    return df




import pandas as pd

def crear_dataframe_secciones(materias, columnas=None):
    """
    Crea un DataFrame con todos los detalles de las secciones y las materias asociadas.
    Renombra las columnas según lo especificado antes de crear el DataFrame.
    """
   
    if not materias:
        raise ValueError("No se encontraron materias para el grado especificado.")
    
    # Mapeo de los nombres de las columnas
    mapeo_columnas = {
        'id_seccion': 'ID Sección',
        'nombre_seccion': 'Nombre Sección',
        'id_grado': 'ID Grado',
        'id_profesor': 'ID Profesor',
        'id_materia': 'ID Materia',
        'nombre_materia': 'Nombre Materia',
        'descripcion_materia': 'Descripción Materia'
    }

    # Renombrar las claves de los diccionarios de resultados
    materias_renombradas = [
        {mapeo_columnas.get(key, key): value for key, value in materia.items()}
        for materia in materias
    ]
    
    # Si no se pasan columnas, se utilizan todas las columnas disponibles
    if not columnas:
        columnas = ["ID Sección", "Nombre Sección", "ID Grado", "ID Profesor", "ID Materia", "Nombre Materia", "Descripción Materia"]
    
    # Crear el DataFrame con los resultados renombrados
    df = pd.DataFrame(materias_renombradas, columns=columnas)
    
    return df
