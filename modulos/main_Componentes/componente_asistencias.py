from modulos import db_conector
import pandas as pd

def obtener_secciones(user_id):
    """Obtiene las secciones asignadas al usuario (profesor)."""
    query = """
    SELECT s."ID_SECCION", s."NOMBRE_SECCION" 
    FROM "SECCIONES" s 
    JOIN "PROFESORES" p ON s."ID_PROF" = p."ID_PROF"
    WHERE p."ID_ACCESO" = %s
    """
    secciones = db_conector.ejecutar_query(query, (user_id,))
    return secciones

def obtener_estudiantes(user_id):
    """Obtiene los estudiantes asignados al usuario (profesor)."""
    query = """
SELECT e."ID_EST", e."NOMBRE_EST", e."APELLIDO_EST", e."CEDULA_EST", s."ID_SECCION", s."NOMBRE_SECCION"
FROM "ESTUDIANTES" e
JOIN "ASIGNACION_EST" a ON e."ID_EST" = a."ID_EST"
JOIN "SECCIONES" s ON a."ID_SECCION" = s."ID_SECCION"
WHERE s."ID_PROF" = (SELECT "ID_PROF" FROM "PROFESORES" WHERE "ID_ACCESO" = %s)

    """
    estudiantes = db_conector.ejecutar_query(query, (user_id,))
    return estudiantes

def registrar_asistencia_estudiante(estudiante, seccion, fecha_asistencia):
    """Registra la asistencia de un estudiante en una sección."""
    query = """
    INSERT INTO "ASISTENCIA_ESTUDIANTES" ("ID_EST", "ID_SECCION", "FECHA_ASISTENCIA", "ESTADO_ASISTENCIA", "YEAR_ESCOLAR")
    VALUES (%s, %s, %s, TRUE, %s)
    """
    # Obtener ID del estudiante a partir de su nombre completo
    nombre, apellido = estudiante.split(" ", 1)
    query_id_est = "SELECT \"ID_EST\" FROM \"ESTUDIANTES\" WHERE \"NOMBRE_EST\" = %s AND \"APELLIDO_EST\" = %s"
    id_estudiante = db_conector.ejecutar_query(query_id_est, (nombre, apellido))[0]['ID_EST']
    
    # Crear la fecha para YEAR_ESCOLAR: primer día del año actual
    year_escolar = f"{pd.to_datetime('today').year}-01-01"
    
    resultado = db_conector.ejecutar_query(query, (id_estudiante, seccion, fecha_asistencia, year_escolar))
    return resultado


def registrar_asistencia_profesor(user_id, seccion):
    """Registra la asistencia del profesor a una sección."""
    query = """
    INSERT INTO "ASISTENCIA_PROFESORES" ("ID_PROF", "ID_SECCION", "FECHA_ASISTENCIA", "ESTADO_ASISTENCIA", "YEAR_ESCOLAR")
    VALUES (%s, %s, CURRENT_DATE, TRUE, EXTRACT(YEAR FROM CURRENT_DATE)::int)
    """
    query_id_prof = "SELECT \"ID_PROF\" FROM \"PROFESORES\" WHERE \"ID_ACCESO\" = %s"
    id_profesor = db_conector.ejecutar_query(query_id_prof, (user_id,))[0]['ID_PROF']
    
    resultado = db_conector.ejecutar_query(query, (id_profesor, seccion))
    return resultado

def obtener_asistencias_estudiantes(seccion, fecha_inicio=None, fecha_fin=None):
    """Obtiene las asistencias de los estudiantes en una sección, con opción de filtrar por rango de fechas."""
    
    if fecha_inicio and fecha_fin:
        # Convertir las fechas a formato de cadena (YYYY-MM-DD) para la consulta SQL
        fecha_inicio_formateada = fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_formateada = fecha_fin.strftime('%Y-%m-%d')
        
        query = """
        SELECT e."NOMBRE_EST", e."APELLIDO_EST", a."FECHA_ASISTENCIA", a."ESTADO_ASISTENCIA", e."ID_EST"
        FROM "ASISTENCIA_ESTUDIANTES" a
        JOIN "ESTUDIANTES" e ON a."ID_EST" = e."ID_EST"
        JOIN "SECCIONES" s ON a."ID_SECCION" = s."ID_SECCION"
        WHERE a."ID_SECCION" = %s AND a."FECHA_ASISTENCIA" BETWEEN %s AND %s
        """
        
        asistencias = db_conector.ejecutar_query(query, (seccion, fecha_inicio_formateada, fecha_fin_formateada))
    
    else:
        query = """
        SELECT e."NOMBRE_EST", e."APELLIDO_EST", a."FECHA_ASISTENCIA", a."ESTADO_ASISTENCIA"
        FROM "ASISTENCIA_ESTUDIANTES" a
        JOIN "ESTUDIANTES" e ON a."ID_EST" = e."ID_EST"
        JOIN "SECCIONES" s ON a."ID_SECCION" = s."ID_SECCION"
        WHERE a."ID_SECCION" = %s
        """
        
        asistencias = db_conector.ejecutar_query(query, (seccion,))
    
    return pd.DataFrame(asistencias)



def modificar_asistencia_estudiante(estudiante, seccion, nuevo_estado):
    """Modifica el estado de asistencia de un estudiante en una sección."""
    query = """
    UPDATE "ASISTENCIA_ESTUDIANTES"
    SET "ESTADO_ASISTENCIA" = %s
    WHERE "ID_EST" = (SELECT "ID_EST" FROM "ESTUDIANTES" WHERE "NOMBRE_EST" = %s AND "APELLIDO_EST" = %s)
    AND "ID_SECCION" = (SELECT "ID_SECCION" FROM "SECCIONES" WHERE "NOMBRE_SECCION" = %s)
    AND "FECHA_ASISTENCIA" = CURRENT_DATE
    """
    nombre, apellido = estudiante.split(" ", 1)
    resultado = db_conector.ejecutar_query(query, (nuevo_estado, nombre, apellido, seccion))
    return resultado

def eliminar_asistencia_por_estudiante_y_fecha(id_estudiante, fecha_asistencia):
    """Elimina el registro de asistencia de un estudiante en una fecha específica."""
    query = """
    DELETE FROM "ASISTENCIA_ESTUDIANTES"
    WHERE "ID_EST" = %s AND "FECHA_ASISTENCIA" = %s
    """
    
    resultado = db_conector.ejecutar_query(query, (id_estudiante, fecha_asistencia))
    return resultado




def obtener_todas_las_secciones():
    
    query = """
    SELECT s."ID_SECCION", s."NOMBRE_SECCION" 
    FROM "SECCIONES" s 
    JOIN "PROFESORES" p ON s."ID_PROF" = p."ID_PROF";
    """
    secciones = db_conector.ejecutar_query(query,)
    return secciones


def obtener_todos_los_estudiantes():
    """Obtiene todos los estudiantes registrados con su ID_SECCION."""
    query = """
    SELECT e."ID_EST", e."NOMBRE_EST", e."APELLIDO_EST", e."CEDULA_EST", s."ID_SECCION", s."NOMBRE_SECCION"
    FROM "ESTUDIANTES" e
    JOIN "ASIGNACION_EST" a ON e."ID_EST" = a."ID_EST"
    JOIN "SECCIONES" s ON a."ID_SECCION" = s."ID_SECCION"
    """
    estudiantes = db_conector.ejecutar_query(query)
    return estudiantes
