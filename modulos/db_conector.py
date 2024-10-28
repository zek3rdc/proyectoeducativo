import mysql.connector
from mysql.connector import Error


# Función para establecer la conexión con la base de datos
def conectar():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='base_eunb',  # Cambia esto al nombre de tu base de datos
            user='root',  # Cambia a tu usuario de MySQL
            password='12345678'  # Cambia a la contraseña de tu MySQL
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Función para cerrar la conexión
def cerrar_conexion(connection):
    if connection.is_connected():
        connection.close()

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
        except Error as e:
            print(f"Error al ejecutar la modificación: {e}")
            return 0  # En caso de error, devuelve 0
        finally:
            cerrar_conexion(connection)
    else:
        return 0

# Consultar estudiantes
def obtener_estudiantes_1():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
SELECT 
    e.id_estudiante,
    e.nombre AS nombre_estudiante,
    e.apellido AS apellido_estudiante,
    e.matricula,
    e.cedula AS cedula_estudiante,
    e.estado,
    e.descripcion AS razon,
    e.genero,                -- Agregar el género del estudiante
    p.id_padres AS id_padre,
    p.nombre AS nombre_padre,
    p.apellido AS apellido_padre,
    p.cedula AS cedula_padre
FROM estudiantes e
JOIN padres_estudiantes pe ON e.id_estudiante = pe.id_estudiante
JOIN padres p ON p.id_padres = pe.id_padres
            """)
            estudiantes = cursor.fetchall()
            return estudiantes
        except Error as e:
            print(f"Error al consultar Estudiantes: {e}")
            return None
        finally:
            cerrar_conexion(connection)



def obtener_secciones():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM secciones")
            secciones = cursor.fetchall()
            
            # Imprimir las secciones para depuración
            print("Secciones obtenidas:", secciones)  # Verifica los datos obtenidos

            # Retorna las secciones obtenidas
            return secciones
        except Error as e:
            print(f"Error al consultar secciones: {e}")
            return None
        finally:
            cerrar_conexion(connection)
def obtener_padres():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM padres")
            estudiantes = cursor.fetchall()
            return estudiantes
        except Error as e:
            print(f"Error al consultar Padres: {e}")
            return None
        finally:
            cerrar_conexion(connection)

def obtener_ultimo_id_estudiante():
    connection = conectar()  # Asegúrate de que esta función esté definida
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT MAX(id_estudiante) AS ultimo_id FROM estudiantes")
            resultado = cursor.fetchone()  # Obtener el resultado de la consulta
            return resultado['ultimo_id'] if resultado['ultimo_id'] is not None else None
        except Error as e:
            print(f"Error al obtener el último ID de estudiante: {e}")
            return None
        finally:
            cerrar_conexion(connection)  # Cierra la conexión
def matricula_existe(matricula):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM estudiantes WHERE matricula = %s", (matricula,))
            result = cursor.fetchone()
            return result['total'] > 0  # Devuelve True si la matrícula existe, False si no
        except Error as e:
            print(f"Error al consultar matrícula: {e}")
            return False  # En caso de error, asumimos que no existe
        finally:
            cerrar_conexion(connection)
def cedula_existe(cedula):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM estudiantes WHERE Cedula = %s", (cedula,))
            result = cursor.fetchone()
            return result['total'] > 0  # Devuelve True si la matrícula existe, False si no
        except Error as e:
            print(f"Error al consultar matrícula: {e}")
            return False  # En caso de error, asumimos que no existe
        finally:
            cerrar_conexion(connection)
def cambiar_estado_estudiante(id_estudiante, nuevo_estado, descripcion):
    try:
        connection = conectar()
        cursor = connection.cursor()
        
        # Actualizar el estado y la descripción del estudiante
        query = """
        UPDATE estudiantes 
        SET estado = %s, descripcion = %s 
        WHERE id_estudiante = %s
        """
        cursor.execute(query, (nuevo_estado, descripcion, id_estudiante))
        connection.commit()
        
        print(f"Estado del estudiante con ID {id_estudiante} actualizado.")
    
    except Error as e:
        print(f"Error al cambiar el estado del estudiante: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
