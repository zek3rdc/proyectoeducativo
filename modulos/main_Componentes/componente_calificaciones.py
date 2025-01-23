from modulos import db_conector
from psycopg2.extras import RealDictCursor
import streamlit as st


# Función para obtener las secciones y calificaciones asignadas al profesor
def obtener_datos_calificaciones(id_acceso):
    query_secciones = """
SELECT 
    S."ID_SECCION", S."NOMBRE_SECCION", G."NOMBRE_GRADO" 
FROM 
    public."SECCIONES" S
JOIN 
    public."GRADOS" G ON S."ID_GRADO" = G."ID_GRADOS"
WHERE 
    S."ID_PROF" = (
        SELECT "ID_PROF" 
        FROM public."PROFESORES" 
        WHERE "ID_ACCESO" = %s
    );

    """
    query_calificaciones = """
SELECT 
    C."ID_CALIFICACION", 
    E."NOMBRE_EST", 
    E."APELLIDO_EST", 
    M."NOMBRE_MATERIA", 
    C."CALIFICACION", 
    C."FECHA_CALIFICACION",
    S."NOMBRE_SECCION"  -- Asegúrate de incluir el nombre de la sección
FROM 
    public."CALIFICACIONES" C
JOIN 
    public."ESTUDIANTES" E ON C."ID_EST" = E."ID_EST"
JOIN 
    public."MATERIAS" M ON C."ID_MATERIA" = M."ID_MATERIA"
JOIN
    public."SECCIONES" S ON C."ID_SECCION" = S."ID_SECCION"  -- Asegúrate de unir la tabla SECCIONES
WHERE 
    C."ID_SECCION" IN (
        SELECT S."ID_SECCION" 
        FROM public."SECCIONES" S
        WHERE S."ID_PROF" = (
            SELECT "ID_PROF" 
            FROM public."PROFESORES" 
            WHERE "ID_ACCESO" = %s
        )
    )


    """
    connection = db_conector.conectar()
    if not connection:
        return None, None
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # Obtener secciones
            cursor.execute(query_secciones, (id_acceso,))
            secciones = cursor.fetchall()
            
            # Obtener calificaciones
            cursor.execute(query_calificaciones, (id_acceso,))
            calificaciones = cursor.fetchall()
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return None, None
    finally:
        connection.close()
    return secciones, calificaciones


# Función para actualizar calificaciones en la base de datos (modulo componente_calificaciones)
def actualizar_calificacion(id_calificacion, nueva_calificacion):
    query = """
        UPDATE public."CALIFICACIONES"
        SET "CALIFICACION" = %s
        WHERE "ID_CALIFICACION" = %s;
    """
    # Ejecutar el query con el ID de calificación y la nueva calificación
    db_conector.ejecutar_query(query, (nueva_calificacion, id_calificacion))