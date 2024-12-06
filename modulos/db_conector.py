import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

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
import psycopg2

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
def obtener_ESTUDIANTES_1():
    connection = conectar()  # Conectar a la base de datos
    if connection:
        try:
            # Usar RealDictCursor para obtener resultados como diccionario
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
            SELECT 
                e.ID_EST,
                e.NOMBRE_EST,
                e.APELLIDO_EST,
                e.CI_EST,
                e.CEDULA_EST,
                e.ESTADO,
                e.DESCRIPCION,
                e.GENERO,                
                p.ID_REP,
                p.NOMBRE_REPRE,
                p.APELLIDO_REPRE,
                p.CEDULA_REPRE
            FROM ESTUDIANTES e
            JOIN REPRE_EST pe ON e.ID_EST = pe.ID_EST
            JOIN REPRESENTANTES p ON p.ID_REP = pe.ID_R                                            EP;
            """)
            
            ESTUDIANTES = cursor.fetchall()  # Obtener todos los resultados de la consulta
            return ESTUDIANTES  # Devuelve la lista de diccionarios
        except psycopg2.OperationalError as e:  # Manejo de errores específico para psycopg2
            print(f"OperationalError al consultar ESTUDIANTES: {e}")
            return None
        finally:
            cerrar_conexion(connection)  # Asegúrate de cerrar la conexión



def obtener_secciones():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM SECCIONES")
            secciones = cursor.fetchall()
            
            # Imprimir las secciones para depuración
            print("Secciones obtenidas:", secciones)  # Verifica los datos obtenidos

            # Retorna las secciones obtenidas
            return secciones
        except OperationalError as e:
            print(f"OperationalError al consultar secciones: {e}")
            return None
        finally:
            cerrar_conexion(connection)
def obtener_padres():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM REPRESENTANTES")
            ESTUDIANTES = cursor.fetchall()
            return ESTUDIANTES
        except OperationalError as e:
            print(f"OperationalError al consultar Representantes: {e}")
            return None
        finally:
            cerrar_conexion(connection)

def obtener_ultimo_ID_EST():
    connection = conectar()  # Asegúrate de que esta función esté definida
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT MAX(ID_EST) AS ULTIMO_ID FROM ESTUDIANTES")
            resultado = cursor.fetchone()  # Obtener el resultado de la consulta
            return resultado['ULTIMO_ID'] if resultado['ULTIMO_ID'] is not None else None
        except OperationalError as e:
            print(f"OperationalError al obtener el último ID de estudiante: {e}")
            return None
        finally:
            cerrar_conexion(connection)  # Cierra la conexión
def matricula_existe(matricula_EST):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT COUNT(*) as total FROM ESTUDIANTES WHERE CEDULA_EST = %s", (matricula_EST,))
            result = cursor.fetchone()
            return result['total'] > 0  # Devuelve True si la matrícula existe, False si no
        except OperationalError as e:
            print(f"OperationalError al consultar matrícula: {e}")
            return False  # En caso de OperationalError, asumimos que no existe
        finally:
            cerrar_conexion(connection)
def cedula_existe(cedula_EST):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT COUNT(*) as total FROM ESTUDIANTES WHERE CEDULA_EST = %s", (cedula_EST,))
            result = cursor.fetchone()
            return result['total'] > 0  # Devuelve True si la matrícula existe, False si no
        except OperationalError as e:
            print(f"OperationalError al consultar matrícula: {e}")
            return False  # En caso de OperationalError, asumimos que no existe
        finally:
            cerrar_conexion(connection)


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
