import pandas as pd

# Función para crear un DataFrame a partir de una lista de diccionarios
def crear_dataframe(data, columnas=None):
    # Convertir la lista de diccionarios a DataFrame
    df = pd.DataFrame(data)
    
    # Si se proporcionan nombres de columnas, renombrar
    if columnas:
        df.columns = columnas
    
    return df
