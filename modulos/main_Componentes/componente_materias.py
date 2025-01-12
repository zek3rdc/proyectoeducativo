from modulos.db_conector import ejecutar_query
from datetime import datetime

# Función para agregar materia sin la fecha de creación
def agregar_materia(nombre, descripcion):
    query = """
        INSERT INTO public."MATERIAS" ("NOMBRE_MATERIA", "DESCRIPCION_MATERIA", "FECHA_CREACION")
        VALUES (%s, %s, NOW())
    """
    return ejecutar_query(query, (nombre, descripcion))

# Función para listar todas las materias
def listar_materias():
    query = 'SELECT * FROM "MATERIAS";'
    resultados = ejecutar_query(query)
    materias = []
    for materia in resultados:
        materias.append({
            "ID_MATERIA": materia["ID_MATERIA"],  # Usar la clave del diccionario
            "NOMBRE_MATERIA": materia["NOMBRE_MATERIA"],  # Usar la clave del diccionario
            "DESCRIPCION_MATERIA": materia["DESCRIPCION_MATERIA"]  # Usar la clave del diccionario
        })
    return materias

# Función para eliminar una materia por su ID
def eliminar_materia(id_materia):
    query = """DELETE FROM public."MATERIAS" WHERE "ID_MATERIA" = %s"""
    return ejecutar_query(query, (id_materia,))

# Función para asignar una materia a una sección con fecha de registro
def asignar_materia_a_seccion(id_materia, id_seccion):
    try:
        # Obtener la fecha actual
        query_insert_materia_seccion = """
            INSERT INTO public."SECCIONES_MATERIAS" ("ID_MATERIA", "ID_SECCION", "FECHA_CREACION")
            VALUES (%s, %s, NOW());
        """
        # Ejecutar la consulta para insertar la materia en la sección
        ejecutar_query(query_insert_materia_seccion, (id_materia, id_seccion))

        # Obtener todos los estudiantes de la sección
        query_estudiantes_seccion = """
            SELECT "ID_EST" 
            FROM public."ASIGNACION_EST"
            WHERE "ID_SECCION" = %s;
        """
        estudiantes = ejecutar_query(query_estudiantes_seccion, (id_seccion,))

        # Asignar la materia a todos los estudiantes de la sección con una calificación de 0
        query_insert_materia_estudiante = """
            INSERT INTO public."CALIFICACIONES" ("ID_EST", "ID_MATERIA", "ID_SECCION", "CALIFICACION", "YEAR_ESCOLAR", "FECHA_CALIFICACION")
            VALUES (%s, %s, %s, 0, NOW(), NOW());
        """
        for estudiante in estudiantes:
            # Ejecutar la consulta para asignar la materia a cada estudiante con calificación 0
            ejecutar_query(query_insert_materia_estudiante, (estudiante['ID_EST'], id_materia, id_seccion))

        return True  # Si todo se ejecutó correctamente

    except Exception as e:
        print(f"Error al asignar la materia a la sección: {e}")
        return False


def actualizar_materia(id_materia, nombre, descripcion):
    query = """
        UPDATE public."MATERIAS"
        SET "NOMBRE_MATERIA" = %s, "DESCRIPCION_MATERIA" = %s
        WHERE "ID_MATERIA" = %s
    """
    return ejecutar_query(query, (nombre, descripcion, id_materia), fetch_all=False)
