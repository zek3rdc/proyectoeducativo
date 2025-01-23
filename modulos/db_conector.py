import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
import pandas as pd

def conectar():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="BASE_EUNB",  # Cambia esto al nombre de tu base de datos
            user="zek3rdc",  # Cambia a tu usuario de PostgreSQL
            password="prueba12P$A"  # Cambia a la contraseña de tu PostgreSQL
        )
        if connection:
            return connection
    except OperationalError as e:
        print(f"OperationalError al conectar a PostgreSQL: {e}")
        return None


# Función para cerrar la conexión

def cerrar_conexion(connection):
    if connection is not None:
        try:
            # Intentamos hacer una consulta simple para verificar si la conexión está activa
            connection.cursor().execute('SELECT 1')
            connection.close()  # Cierra la conexión a PostgreSQL
            print("Conexión cerrada exitosamente.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")


# Función para ejecutar una consulta INSERT, UPDATE o DELETE
def ejecutar_modificacion(query, parametros=None):
    connection = conectar()  # Llamar a la función que conecta a MySQL
    if connection is not None:
        try:
            cursor = connection.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor.rowcount  # Retorna el número de filas afectadas
        except OperationalError as e:
            print(f"OperationalError al ejecutar la modificación: {e}")
            return 0  # En caso de OperationalError, devuelve 0
        finally:
            cerrar_conexion(connection)
    else:
        return 0

# Consultar ESTUDIANTES
# Consultar ESTUDIANTES
def obtener_ESTUDIANTES_1():
    connection = conectar()  # Conectar a la base de datos
    if connection:
        try:
            # Usar RealDictCursor para obtener resultados como diccionario
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
SELECT 
    e."ID_EST",
    e."NOMBRE_EST",
    e."APELLIDO_EST",
    e."CEDULA" AS "CI_EST",  -- Columna corregida según la definición de la base de datos
    e."CEDULA_EST",
    e."EMAIL_EST",
    e."TELEFONO_EST",                                               
    e."ESTADO",
    e."DESCRIPCION_ESTADO" AS "DESCRIPCION",  -- Usar la columna correcta
    e."GENERO",
    e."CONDICION",
    p."ID_REP",
    p."NOMBRE_REP" AS "NOMBRE_REPRE",
    p."APELLIDO_REP" AS "APELLIDO_REPRE",
    p."CEDULA_REP",
    e."FECHA_REG",
    s."NOMBRE_SECCION" AS "SECCION_ASIGNADA"  -- Agregar la sección asignada
FROM 
    "ESTUDIANTES" e
JOIN 
    "REPRE_EST" pe ON e."ID_EST" = pe."ID_EST"
JOIN 
    "REPRESENTANTES" p ON p."ID_REP" = pe."ID_REPRE"
LEFT JOIN 
    "ASIGNACION_EST" ae ON e."ID_EST" = ae."ID_EST"  -- Relación con la tabla de asignaciones
LEFT JOIN 
    "SECCIONES" s ON ae."ID_SECCION" = s."ID_SECCION"  -- Obtener el nombre de la sección
            """)
            
            # Obtener todos los resultados de la consulta
            estudiantes = cursor.fetchall()
            return estudiantes  # Devuelve la lista de diccionarios
        except psycopg2.OperationalError as e:  # Manejo de errores específico para psycopg2
            print(f"OperationalError al consultar ESTUDIANTES: {e}")
            return None
        except psycopg2.Error as e:  # Manejo de otros errores de psycopg2
            print(f"Error al consultar ESTUDIANTES: {e}")
            return None
        finally:
            cerrar_conexion(connection)  # Asegúrate de cerrar la conexión



def obtener_padres():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""SELECT * FROM public."REPRESENTANTES" ORDER BY "ID_REP" ASC """)
            ESTUDIANTES = cursor.fetchall()
            return ESTUDIANTES
        except OperationalError as e:
            print(f"OperationalError al consultar Representantes: {e}")
            return None
        finally:
            cerrar_conexion(connection)

def obtener_ultimo_ID_EST():
    connection = conectar()  # Asegúrate de que esta función esté definida para conectar a la base de datos
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            # Ejecutar la consulta para obtener el último ID de estudiante
            cursor.execute("""SELECT MAX("ID_EST") AS ULTIMO_ID FROM "ESTUDIANTES";""")
            resultado = cursor.fetchone()  # Obtener el resultado de la consulta
            
            # Devolver el último ID, o None si no existe
            return resultado['ULTIMO_ID'] if resultado['ULTIMO_ID'] is not None else None
        except OperationalError as e:
            print(f"OperationalError al obtener el último ID de estudiante: {e}")
            return None
        except Exception as e:
            # Captura de otros errores para proporcionar más detalles
            print(f"Error inesperado: {e}")
            return None
        finally:
            cerrar_conexion(connection)  # Cierra la conexión al final

def registro_existe(tabla, campo, valor):
    """
    Verifica si un registro existe en una tabla específica.
    """
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            query = f"""SELECT COUNT(*) as total FROM "{tabla}" WHERE "{campo}" = %s"""
            cursor.execute(query, (valor,))
            result = cursor.fetchone()
            return result['total'] > 0
        except Exception as e:
            print(f"Error al consultar registro en {tabla}.{campo}={valor}: {e}")
            return False
        finally:
            cerrar_conexion(connection)



def matricula_existe(cedula_EST):
    """
    Verifica si una matrícula existe en la tabla ESTUDIANTES.
    """
    return registro_existe("ESTUDIANTES", "CEDULA_EST", cedula_EST)

def cedula_existe(cedula):
    """
    Verifica si una cédula existe en la tabla ESTUDIANTES.
    """
    return registro_existe("ESTUDIANTES", "CEDULA", cedula)



def cambiar_estado_estudiante(ID_EST, nuevo_estado, descripcion):
    try:
        connection = conectar()
        cursor = connection.cursor()
        
        # Actualizar el estado y la descripción del estudiante
        query = """
        UPDATE ESTUDIANTES 
        SET ESTADO = %s, DESCRIPCION = %s 
        WHERE ID_EST = %s
        """
        cursor.execute(query, (nuevo_estado, descripcion, ID_EST))
        connection.commit()
        
        print(f"Estado del estudiante con ID {ID_EST} actualizado.")
    
    except OperationalError as e:
        print(f"OperationalError al cambiar el estado del estudiante: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def ejecutar_consulta_unica(query, parametros):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, parametros)
            result = cursor.fetchone()
            connection.commit()
            return result
        finally:
            cerrar_conexion(connection)




def obtener_datos(query, parametros=None):
    """
    Ejecuta una consulta SELECT y devuelve los resultados.
    
    :param query: La consulta SQL a ejecutar.
    :param parametros: Parámetros opcionales para la consulta.
    :return: Lista de resultados.
    """
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            resultados = cursor.fetchall()  # Obtener todos los resultados
            cursor.close()
            conn.close()
            return resultados
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
        finally:
            if conn:
                conn.close()
    return []



def obtener_secciones():
    """
    Obtiene las secciones con su grado y profesor.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT 
            s."ID_SECCION", 
            s."NOMBRE_SECCION" AS "NOMBRE_SECCION",  -- Renombrando aquí
            g."NOMBRE_GRADO", 
            p."NOMBRE_PROF" || ' ' || p."APELLIDO_PROF" AS "PROFESOR"
        FROM 
            public."SECCIONES" s
        JOIN 
            public."GRADOS" g ON s."ID_GRADO" = g."ID_GRADOS"
        JOIN 
            public."PROFESORES" p ON s."ID_PROF" = p."ID_PROF"
        ORDER BY 
            s."ID_SECCION";

        """
        cursor.execute(query)
        secciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return secciones
    except Exception as e:
        print(f"Error al obtener secciones: {e}")
        return []

def obtener_materias_por_grado(grado):
    """
    Obtiene las materias asignadas a un grado.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT 
            m."NOMBRE_MATERIA"
        FROM 
            public."GRADO_MATERIAS" gm
        JOIN 
            public."GRADOS" g ON gm."ID_GRADO" = g."ID_GRADOS"
        JOIN 
            public."MATERIAS" m ON gm."ID_MATERIA" = m."ID_MATERIA"
        WHERE 
            g."NOMBRE_GRADO" = %s;
        """
        cursor.execute(query, (grado,))
        materias = cursor.fetchall()
        cursor.close()
        conn.close()
        return [materia[0] for materia in materias]
    except Exception as e:
        print(f"Error al obtener materias por grado: {e}")
        return []

def obtener_asistencia_estudiantes(id_seccion):
    """
    Obtiene la asistencia de los estudiantes para una sección.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT 
            e."NOMBRE_EST" || ' ' || e."APELLIDO_EST" AS "ESTUDIANTE",
            a."FECHA_ASISTENCIA",
            a."ESTADO_ASISTENCIA"
        FROM 
            public."ASISTENCIA_ESTUDIANTES" a
        JOIN 
            public."ESTUDIANTES" e ON a."ID_EST" = e."ID_EST"
        WHERE 
            a."ID_SECCION" = %s;
        """
        cursor.execute(query, (id_seccion,))
        asistencia = cursor.fetchall()
        cursor.close()
        conn.close()
        return asistencia
    except Exception as e:
        print(f"Error al obtener asistencia de estudiantes: {e}")
        return []

def obtener_asistencia_profesores(id_seccion):
    """
    Obtiene la asistencia del profesor para una sección.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT 
            p."NOMBRE_PROF" || ' ' || p."APELLIDO_PROF" AS "PROFESOR",
            a."FECHA_ASISTENCIA",
            a."ESTADO_ASISTENCIA"
        FROM 
            public."ASISTENCIA_PROFESORES" a
        JOIN 
            public."PROFESORES" p ON a."ID_PROF" = p."ID_PROF"
        WHERE 
            a."ID_SECCION" = %s;
        """
        cursor.execute(query, (id_seccion,))
        asistencia = cursor.fetchall()
        cursor.close()
        conn.close()
        return asistencia
    except Exception as e:
        print(f"Error al obtener asistencia de profesores: {e}")
        return []

def obtener_calificaciones_estudiantes(id_seccion):
    """
    Obtiene las calificaciones de los estudiantes para una sección.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = """
        SELECT 
            e."NOMBRE_EST" || ' ' || e."APELLIDO_EST" AS "ESTUDIANTE",
            m."NOMBRE_MATERIA",
            c."CALIFICACION"
        FROM 
            public."CALIFICACIONES" c
        JOIN 
            public."ESTUDIANTES" e ON c."ID_EST" = e."ID_EST"
        JOIN 
            public."MATERIAS" m ON c."ID_MATERIA" = m."ID_MATERIA"
        WHERE 
            c."ID_SECCION" = %s;
        """
        cursor.execute(query, (id_seccion,))
        calificaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return calificaciones
    except Exception as e:
        print(f"Error al obtener calificaciones de estudiantes: {e}")
        return []




def ejecutar_query(query, parametros=None, fetch_all=True):
    """
    Ejecuta una consulta SQL en la base de datos PostgreSQL.

    Parámetros:
    - query (str): La consulta SQL a ejecutar.
    - parametros (tuple): Los parámetros para la consulta (opcional).
    - fetch_all (bool): Si es True, recupera todos los resultados (SELECT). 
                        Si es False, recupera solo un resultado.

    Retorna:
    - Lista de resultados (para SELECT con fetch_all=True).
    - Un único resultado (para SELECT con fetch_all=False).
    - True (para consultas que no devuelven datos, como INSERT, UPDATE o DELETE).
    - None si ocurre un error.
    """
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, parametros)

            if cursor.description:  # Verifica si hay datos para recuperar (SELECT)
                if fetch_all:
                    return cursor.fetchall()  # Recupera todos los resultados
                else:
                    return cursor.fetchone()  # Recupera un único resultado
            else:
                connection.commit()  # Confirmar cambios para INSERT, UPDATE o DELETE
                return True

        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

        finally:
            cerrar_conexion(connection)
    else:
        print("No se pudo establecer conexión con la base de datos.")
        return None




def listar_secciones():
    """
    Obtiene la lista de secciones desde la base de datos.
    """
    query = '''
        SELECT 
            "ID_SECCION" AS id_seccion, 
            "NOMBRE_SECCION" AS nombre_seccion, 
            "ID_GRADO" AS grado, 
            "ID_PROF" AS profesor
        FROM public."SECCIONES";
    '''
    return ejecutar_query(query)

def listar_detalles_seccion(id_seccion):
    """
    Obtiene todos los detalles de las secciones y las materias asociadas a una sección.
    """
    if not isinstance(id_seccion, int):
        raise ValueError(f"El ID de la sección debe ser un número entero. Se recibió: {id_seccion}")

    query = '''
        SELECT 
            s."ID_SECCION" AS id_seccion,
            s."NOMBRE_SECCION" AS nombre_seccion,
            s."ID_GRADO" AS id_grado,
            g."NOMBRE_GRADO" AS nombre_grado,  -- Nombre del grado
            p."NOMBRE_PROF" AS nombre_profesor,     -- Nombre del profesor (ajustado)
            p."CEDULA_PROF" AS cedula_profesor,     -- Cédula del profesor (ajustado)
            m."ID_MATERIA" AS id_materia,
            m."NOMBRE_MATERIA" AS nombre_materia,
            m."DESCRIPCION_MATERIA" AS descripcion_materia
        FROM public."SECCIONES_MATERIAS" sm
        INNER JOIN public."SECCIONES" s ON sm."ID_SECCION" = s."ID_SECCION"
        INNER JOIN public."MATERIAS" m ON sm."ID_MATERIA" = m."ID_MATERIA"
        INNER JOIN public."GRADOS" g ON s."ID_GRADO" = g."ID_GRADOS"  -- Ajuste aquí: la columna de grados es "ID_GRADOS"
        INNER JOIN public."PROFESORES" p ON s."ID_PROF" = p."ID_PROF"  -- Relación con la tabla de profesores
        WHERE s."ID_SECCION" = %s;  -- Filtrar por el ID de la sección
    '''
    return ejecutar_query(query, (id_seccion,))



def listar_asistencia_estudiantes(id_seccion):
    """
    Obtiene los datos de asistencia de los estudiantes de una sección específica.
    """
    query = '''
        SELECT 
            ae."ID_EST" AS id_estudiante, 
            e."NOMBRE_EST" AS nombre, 
            ae."FECHA_ASISTENCIA" AS fecha, 
            ae."ESTADO_ASISTENCIA" AS estado
        FROM public."ASISTENCIA_ESTUDIANTES" ae
        INNER JOIN public."ESTUDIANTES" e ON ae."ID_EST" = e."ID_EST"
        WHERE ae."ID_SECCION" = %s;
    '''
    return ejecutar_consulta_unica(query, (id_seccion,))

def listar_asistencia_profesores(id_seccion):
    """
    Obtiene los datos de asistencia del profesor de una sección específica.
    """
    query = '''
        SELECT 
            ap."ID_PROF" AS id_profesor, 
            p."NOMBRE_PROF" AS nombre, 
            ap."FECHA_ASISTENCIA" AS fecha, 
            ap."ESTADO_ASISTENCIA" AS estado
        FROM public."ASISTENCIA_PROFESORES" ap
        INNER JOIN public."PROFESORES" p ON ap."ID_PROF" = p."ID_PROF"
        WHERE ap."ID_SECCION" = %s;
    '''
    return ejecutar_consulta_unica(query, (id_seccion,))

def listar_calificaciones(id_seccion):
    """
    Obtiene las calificaciones de los estudiantes en una sección específica.
    """
    query = '''
        SELECT 
            c."ID_EST" AS id_estudiante, 
            e."NOMBRE_EST" AS nombre, 
            m."NOMBRE_MATERIA" AS materia, 
            c."CALIFICACION" AS calificacion, 
            c."FECHA_CALIFICACION" AS fecha
        FROM public."CALIFICACIONES" c
        INNER JOIN public."ESTUDIANTES" e ON c."ID_EST" = e."ID_EST"
        INNER JOIN public."MATERIAS" m ON c."ID_MATERIA" = m."ID_MATERIA"
        WHERE c."ID_SECCION" = %s;
    '''
    return ejecutar_consulta_unica(query, (id_seccion,))

def listar_profesores():
    """
    Obtiene la lista de profesores desde la base de datos, incluyendo aquellos sin rol asignado.
    """
    query = '''
SELECT 
    p."ID_PROF" AS id_profesor,
    p."NOMBRE_PROF" AS nombre,
    p."APELLIDO_PROF" AS apellido,
    p."CEDULA_PROF" AS cedula,
    p."TELEFONO_PROF" AS telefono,
    p."DIRECCION_PROF" AS direccion,
    p."EMAIL_PROF" AS email,
    COALESCE(r."ROL", 'Sin Rol') AS rol  -- Si no tiene rol, mostramos 'Sin Rol'
FROM 
    public."PROFESORES" p
LEFT JOIN 
    public."ROLES" r 
ON 
    p."ID_ROL" = r."ID_ROL";

    '''
    return ejecutar_query(query)

def obtener_secciones_rendimiento():
    """
    Obtiene las secciones desde la base de datos.
    """
    query = '''
        SELECT DISTINCT "ID_SECCION", "NOMBRE_SECCION"
        FROM public."SECCIONES";
    '''
    resultados = ejecutar_query(query)
    return [f"{row['ID_SECCION']} - {row['NOMBRE_SECCION']}" for row in resultados]

def obtener_materias():
    """
    Obtiene las materias desde la base de datos.
    """
    query = '''
        SELECT DISTINCT "ID_MATERIA", "NOMBRE_MATERIA"
        FROM public."MATERIAS";
    '''
    resultados = ejecutar_query(query)
    return [f"{row['ID_MATERIA']} - {row['NOMBRE_MATERIA']}" for row in resultados]

def obtener_anios_escolares():
    """
    Obtiene los años escolares desde la base de datos.
    """
    query = '''
        SELECT DISTINCT "YEAR_ESCOLAR"
        FROM public."CALIFICACIONES"
        ORDER BY "YEAR_ESCOLAR" DESC;
    '''
    resultados = ejecutar_query(query)
    return [row['YEAR_ESCOLAR'] for row in resultados]

def obtener_calificaciones(seccion, materia, year_escolar):
    """
    Obtiene las calificaciones filtradas por sección, materia y año escolar.
    """
    condiciones = []
    parametros = []

    # Agregar condiciones dinámicas basadas en los filtros
    if seccion != "Ver Todo":
        id_seccion = seccion.split(" - ")[0]
        condiciones.append('cal."ID_SECCION" = %s')
        parametros.append(id_seccion)

    if materia != "Ver Todo":
        id_materia = materia.split(" - ")[0]
        condiciones.append('cal."ID_MATERIA" = %s')
        parametros.append(id_materia)

    if year_escolar != "Ver Todo":
        condiciones.append('cal."YEAR_ESCOLAR" = %s')
        parametros.append(year_escolar)

    # Construir el WHERE dinámico
    where_clause = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    query = f'''
        SELECT 
            est."ID_EST",
            est."NOMBRE_EST",
            est."APELLIDO_EST",
            cal."CALIFICACION",
            mat."NOMBRE_MATERIA",
            sec."NOMBRE_SECCION",
            cal."YEAR_ESCOLAR",
            cal."FECHA_CALIFICACION"
        FROM public."CALIFICACIONES" cal
        JOIN public."ESTUDIANTES" est ON cal."ID_EST" = est."ID_EST"
        JOIN public."MATERIAS" mat ON cal."ID_MATERIA" = mat."ID_MATERIA"
        JOIN public."SECCIONES" sec ON cal."ID_SECCION" = sec."ID_SECCION"
        {where_clause}
        ORDER BY cal."FECHA_CALIFICACION" DESC;
    '''
    resultados = ejecutar_query(query, parametros)
    return pd.DataFrame(resultados)

def asignar_estudiante_a_seccion(id_estudiante, id_seccion):
    """
    Asigna un estudiante a una sección específica y le asigna las materias de esa sección.
    Args:
        id_estudiante (int): ID del estudiante.
        id_seccion (int): ID de la sección a asignar.
    Returns:
        bool: True si la asignación fue exitosa, False si hubo un error.
    """
    try:
        # Asegurarse de que los IDs sean de tipo int
        id_estudiante = int(id_estudiante)
        id_seccion = int(id_seccion)

        # Conectar a la base de datos
        conn = conectar()  # Usamos la función que ya tienes para conectar a la base de datos
        cursor = conn.cursor()

        # Verificar si el estudiante ya está asignado a la sección
        query_check = """
        SELECT COUNT(*) 
        FROM "ASIGNACION_EST"
        WHERE "ID_EST" = %s AND "ID_SECCION" = %s;
        """
        cursor.execute(query_check, (id_estudiante, id_seccion))
        result = cursor.fetchone()
        if result[0] > 0:
            # El estudiante ya está asignado a esta sección
            print(f"El estudiante {id_estudiante} ya está asignado a la sección {id_seccion}.")
            cursor.close()
            conn.close()
            return False

        # Insertar la asignación del estudiante a la sección
        query_insert = """
        INSERT INTO "ASIGNACION_EST" ("ID_EST", "ID_SECCION", "YEAR_ESCOLAR", "FECHA_ASIGNACION")
        VALUES (%s, %s, NOW(), NOW());
        """
        cursor.execute(query_insert, (id_estudiante, id_seccion))
        conn.commit()  # Confirmar la asignación del estudiante a la sección

        # Obtener las materias asociadas a la sección
        query_materias = """
        SELECT "ID_MATERIA" 
        FROM "SECCIONES_MATERIAS"
        WHERE "ID_SECCION" = %s;
        """
        cursor.execute(query_materias, (id_seccion,))
        materias = cursor.fetchall()

        if not materias:
            print("La sección no tiene materias asignadas.")
            cursor.close()
            conn.close()
            return False

        # Asignar las materias al estudiante con una calificación de 0
        query_insert_calificacion = """
        INSERT INTO "CALIFICACIONES" ("ID_EST", "ID_MATERIA", "ID_SECCION", "CALIFICACION", "YEAR_ESCOLAR", "FECHA_CALIFICACION")
        VALUES (%s, %s, %s, 0, NOW(), NOW());
        """
        for materia in materias:
            cursor.execute(query_insert_calificacion, (id_estudiante, materia[0], id_seccion))
        
        conn.commit()  # Confirmar las calificaciones

        # Cerrar la conexión
        cursor.close()
        conn.close()

        return True  # La asignación fue exitosa
    except Exception as e:
        print(f"Error al asignar el estudiante a la sección: {e}")
        if conn:
            conn.rollback()  # Revertir cambios en caso de error
        return False  # Retornamos False en caso de error

def obtener_estudiantes_por_seccion(id_seccion):
    """
    Obtiene los estudiantes asignados a una sección específica.

    Args:
        id_seccion (int): ID de la sección para la cual se desea obtener los estudiantes.

    Returns:
        list: Lista de tuplas con los datos de los estudiantes 
              (ID_EST, NOMBRE_EST, APELLIDO_EST, CEDULA).
              Retorna una lista vacía si no hay estudiantes o si ocurre un error.
    """
    try:
        # Convertir id_seccion a un entero estándar
        id_seccion = int(id_seccion)

        # Conectar a la base de datos
        conn = conectar()
        cursor = conn.cursor()

        # Query para obtener estudiantes por sección
        query = """
        SELECT 
            e."ID_EST",
            e."NOMBRE_EST",
            e."APELLIDO_EST",
            e."CEDULA",
            e."CEDULA_EST"
        FROM 
            public."ESTUDIANTES" e
        JOIN 
            public."ASIGNACION_EST" ae ON e."ID_EST" = ae."ID_EST"
        WHERE 
            ae."ID_SECCION" = %s
        ORDER BY 
            e."NOMBRE_EST";
        """
        # Ejecutar el query
        cursor.execute(query, (id_seccion,))
        estudiantes = cursor.fetchall()

        # Cerrar cursor y conexión
        cursor.close()
        conn.close()

        # Retornar los resultados
        return estudiantes

    except Exception as e:
        print(f"Error al obtener estudiantes por sección: {e}")
        return []


def insertar_id_acceso_en_base_de_datos(id_profesor, id_acceso):
    """
    Inserta el ID_ACCESO generado en la base de datos para el profesor.
    """
    try:
        connection = conectar()  # Función para conectar a la base de datos
        if connection:
            with connection.cursor() as cursor:
                # Actualizar la tabla "PROFESORES" con el nuevo ID_ACCESO
                query = """
                    UPDATE public."PROFESORES"
                    SET "ID_ACCESO" = %s
                    WHERE "ID_PROF" = %s
                """
                cursor.execute(query, (id_acceso, id_profesor))
                connection.commit()
            return "ID de acceso actualizado exitosamente en la base de datos."
        else:
            return "Error al conectar a la base de datos."
    except Exception as e:
        return f"Error al actualizar ID de acceso en la base de datos: {e}"

