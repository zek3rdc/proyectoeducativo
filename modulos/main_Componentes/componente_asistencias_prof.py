import psycopg2
from modulos.db_conector import conectar
import pandas as pd

def obtener_roles():
    try:
        connection = conectar()
        cursor = connection.cursor()
        query = 'SELECT "ID_ROL", "ROL" FROM public."ROLES"'
        cursor.execute(query)
        roles = cursor.fetchall()
        cursor.close()
        connection.close()
        return {rol[0]: rol[1] for rol in roles}
    except Exception as e:
        print(f"Error al obtener roles: {e}")
        return []

def obtener_personal():
    try:
        connection = conectar()
        cursor = connection.cursor()
        query = '''SELECT p."ID_PROF", p."NOMBRE_PROF", p."APELLIDO_PROF", p."CEDULA_PROF", 
                          p."ID_ROL", r."ROL"
                   FROM public."PROFESORES" p
                   JOIN public."ROLES" r ON p."ID_ROL" = r."ID_ROL"'''
        cursor.execute(query)
        personal = cursor.fetchall()
        cursor.close()
        connection.close()
        return [{
            'ID_PERSONAL': p[0],
            'NOMBRE_PERSONAL': p[1],
            'APELLIDO_PERSONAL': p[2],
            'CEDULA_PERSONAL': p[3],
            'ID_ROL': p[4],
            'ROL': p[5]
        } for p in personal]
    except Exception as e:
        print(f"Error al obtener personal: {e}")
        return []

def registrar_asistencia_personal(id_personal, fecha_asistencia, asistio, justificacion):
    try:
        connection = conectar()
        cursor = connection.cursor()
        query = '''
            INSERT INTO public."ASISTENCIA_PROFESORES" ("ID_PROF", "FECHA_ASISTENCIA", "ESTADO_ASISTENCIA", 
                                                     "JUSTIFICACION", "YEAR_ESCOLAR")
            VALUES (%s, %s, %s, %s, %s)
        '''
        year_escolar = fecha_asistencia.year  # Suponiendo que el "year_escolar" es el año de la fecha
        cursor.execute(query, (id_personal, fecha_asistencia, asistio, justificacion, year_escolar))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al registrar asistencia: {e}")
        return False


def obtener_asistencias_personal(id_personal, fecha_inicio, fecha_fin):
    try:
        connection = conectar()
        cursor = connection.cursor()
        query = '''
            SELECT "FECHA_ASISTENCIA", "ESTADO_ASISTENCIA", "JUSTIFICACION"
            FROM public."ASISTENCIA_PROFESORES"
            WHERE "ID_PROF" = %s AND "FECHA_ASISTENCIA" BETWEEN %s AND %s
        '''
        cursor.execute(query, (id_personal, fecha_inicio, fecha_fin))
        asistencias = cursor.fetchall()
        cursor.close()
        connection.close()
        return pd.DataFrame(asistencias, columns=["Fecha", "Asistió", "Justificación"])
    except Exception as e:
        print(f"Error al obtener asistencias: {e}")
        return pd.DataFrame()

def modificar_asistencia_estudiante(id_personal, fecha_asistencia, estado_asistencia, justificacion):
    try:
        connection = conectar()
        cursor = connection.cursor()
        query = '''
            UPDATE public."ASISTENCIA_PROFESORES"
            SET "ESTADO_ASISTENCIA" = %s, "JUSTIFICACION" = %s
            WHERE "ID_PROF" = %s AND "FECHA_ASISTENCIA" = %s
        '''
        cursor.execute(query, (estado_asistencia, justificacion, id_personal, fecha_asistencia))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al modificar asistencia: {e}")
        return False


def obtener_asistencias_por_rol(id_rol, fecha_inicio, fecha_fin):
    """
    Obtiene las asistencias de los profesores asociados a un rol dentro de un rango de fechas.

    :param id_rol: ID del rol seleccionado.
    :param fecha_inicio: Fecha de inicio del filtro.
    :param fecha_fin: Fecha de fin del filtro.
    :return: DataFrame con las asistencias del personal.
    """
    try:
        connection = conectar()
        if connection is None:
            return pd.DataFrame()

        query = """
SELECT a."ID_PROF", p."NOMBRE_PROF", p."APELLIDO_PROF", a."FECHA_ASISTENCIA", 
       a."ESTADO_ASISTENCIA", a."JUSTIFICACION"
FROM "ASISTENCIA_PROFESORES" a
JOIN "PROFESORES" p ON a."ID_PROF" = p."ID_PROF"
WHERE p."ID_ROL" = %s AND a."FECHA_ASISTENCIA" BETWEEN %s AND %s;

        """

        df_asistencias = pd.read_sql(query, connection, params=(id_rol, fecha_inicio, fecha_fin))
        connection.close()
        return df_asistencias

    except Exception as e:
        print(f"Error al obtener asistencias por rol: {e}")
        return pd.DataFrame()
    
def actualizar_asistencia_profesor(id_prof, fecha_asistencia, estado_asistencia, justificacion):
    """
    Actualiza el estado de asistencia y justificación de un profesor en una fecha específica.

    :param id_prof: ID del profesor.
    :param fecha_asistencia: Fecha de la asistencia.
    :param estado_asistencia: Estado de asistencia (True o False).
    :param justificacion: Justificación (True o False).
    :return: True si la actualización fue exitosa, False en caso contrario.
    """
    try:
        # Asegurarse de que los parámetros sean del tipo adecuado
        id_prof = int(id_prof)  # Convertir id_prof a int si es necesario
        estado_asistencia = bool(estado_asistencia)  # Asegurarse de que sea un booleano
        justificacion = bool(justificacion)  # Asegurarse de que sea un booleano

        connection = conectar()
        if connection is None:
            return False

        cursor = connection.cursor()
        query = """
        UPDATE "ASISTENCIA_PROFESORES"
        SET "ESTADO_ASISTENCIA" = %s, "JUSTIFICACION" = %s
        WHERE "ID_PROF" = %s AND "FECHA_ASISTENCIA" = %s;
        """
        cursor.execute(query, (estado_asistencia, justificacion, id_prof, fecha_asistencia))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"Error al actualizar asistencia: {e}")
        return False

