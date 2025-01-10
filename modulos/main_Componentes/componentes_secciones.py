from datetime import date
from modulos import db_conector  # Asumiendo que db_conector es el archivo donde manejas la conexión con la base de datos
import streamlit as st

def agregar_seccion_db(nombre_seccion, grado_id, profesor_id):
    """
    Inserta una nueva sección en la base de datos.
    
    :param nombre_seccion: Nombre de la nueva sección.
    :param grado_id: ID del grado seleccionado.
    :param profesor_id: ID del profesor seleccionado.
    """
    try:
        # Obtener la fecha actual
        fecha_creacion = date.today()
        
        # Consulta SQL para agregar la nueva sección
        query_agregar_seccion = """
        INSERT INTO public."SECCIONES" ("NOMBRE_SECCION", "ID_GRADO", "ID_PROF", "FECHA_CREA_ASIG")
        VALUES (%s, %s, %s, %s)
        """
        
        # Imprimir los valores para depuración
        print(f"Insertando sección: nombre_seccion={nombre_seccion}, grado_id={grado_id}, profesor_id={profesor_id}, fecha_creacion={fecha_creacion}")
        
        # Ejecutar la consulta en la base de datos
        db_conector.ejecutar_modificacion(query_agregar_seccion, 
            (nombre_seccion, grado_id, profesor_id, fecha_creacion))
        
        return True
    except Exception as e:
        print(f"Error al agregar la sección: {e}")
        return False



def obtener_profesores():
    try:
        query = "SELECT \"ID_PROF\", \"NOMBRE_PROF\", \"APELLIDO_PROF\",\"CEDULA_PROF\"  FROM public.\"PROFESORES\" ORDER BY \"NOMBRE_PROF\";"
        return db_conector.obtener_datos(query)
    except Exception as e:
        st.error(f"Error al obtener los profesores: {e}")
        return []

def editar_seccion_db(id_seccion, nuevo_nombre, id_grado, id_profesor):
    try:
        query = """
        UPDATE public."SECCIONES"
        SET "NOMBRE_SECCION" = %s, "ID_GRADO" = %s, "ID_PROF" = %s
        WHERE "ID_SECCION" = %s;
        """
        parametros = (nuevo_nombre, id_grado, id_profesor, id_seccion)
        
        # Ejecutamos la consulta de actualización
        db_conector.ejecutar_modificacion(query, parametros)
        
        return True
    except Exception as e:
        print(f"Error al editar la sección: {e}")
        return False

def obtener_grados():
    try:
        # Definir el query SQL para obtener los grados
        query = """
        SELECT "ID_GRADOS", "NOMBRE_GRADO" 
        FROM public."GRADOS" 
        ORDER BY "NOMBRE_GRADO";
        """
        
        # Llamar a la función obtener_datos que se encarga de la conexión y ejecución del query
        grados = db_conector.obtener_datos(query)
        
        return grados
    
    except Exception as e:
        # En caso de error, mostrar el mensaje y retornar una lista vacía
        st.error(f"Error al obtener los grados: {e}")
        return []

def rename_fields(materias):
    """
    Renombra las columnas de las materias y devuelve la lista de diccionarios con las columnas renombradas.
    """
    if not materias:
        raise ValueError("No se encontraron materias para el grado especificado.")
    
    # Mapeo de los nombres de las columnas
    mapeo_columnas = {
        'id_seccion': 'ID Sección',
        'nombre_seccion': 'Nombre Sección',
        'id_grado': 'ID Grado',
        'nombre_grado': 'Nombre Grado',  # Nuevo campo
        'id_profesor': 'ID Profesor',
        'nombre_profesor': 'Nombre Profesor',  # Nuevo campo
        'cedula_profesor': 'Cédula Profesor',  # Nuevo campo
        'id_materia': 'ID Materia',
        'nombre_materia': 'Nombre Materia',
        'descripcion_materia': 'Descripción Materia'
    }

    # Renombrar las claves de los diccionarios de resultados
    materias_renombradas = [
        {mapeo_columnas.get(key, key): value for key, value in materia.items()}
        for materia in materias
    ]
    
    return materias_renombradas