from modulos import db_conector
import pandas as pd
import datetime
import os
from PIL import Image
import streamlit as st
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

def renombrar_columnas(df):
    return df.rename(columns={
        'ID_EST': 'ID Estudiante',
        'NOMBRE_EST': 'Nombre Estudiante',
        'APELLIDO_EST': 'Apellido Estudiante',
        'CI_EST': 'Cédula Identidad',
        'CEDULA_EST': 'Cédula Estudiantil',
        "TELEFONO_EST": "Telefono Estudiante",
        "EMAIL_EST": "Email Estudiante",
        'ESTADO': 'Estado',
        'DESCRIPCION': 'Descripción Estado',
        'GENERO': 'Género',
        'CONDICION': 'Condición',
        'ID_REP': 'ID Representante',
        'NOMBRE_REPRE': 'Nombre Representante',
        'APELLIDO_REPRE': 'Apellido Representante',
        'CEDULA_REP': 'Cédula Representante',
        'FECHA_REG': 'Fecha de Registro',
        'SECCION_ASIGNADA': 'Sección Asignada'
    })

# Agregar un estudiante
def agregar_estudiante(nombre, apellido, cedula, cedula_est, id_representante, genero, estado, condicion, fecha_nac, email, telefono):
    try:


        # Validar si la cédula ya existe (solo si no es NULL)
        if cedula and db_conector.cedula_existe(cedula):
            return f"⚠️ La cédula {cedula} ya está registrada en la base de datos."

        # Validar si la matrícula ya existe (solo si no es NULL)
        if cedula_est and db_conector.matricula_existe(cedula_est):
            return f"⚠️ La matrícula {cedula_est} ya está registrada en la base de datos."

        # Insertar el estudiante
        query_agregar_estudiante = """
                INSERT INTO "ESTUDIANTES" (
                    "NOMBRE_EST", "APELLIDO_EST", "CEDULA", "CEDULA_EST", 
                    "GENERO", "ESTADO", "CONDICION", "FECHA_NAC", 
                    "FECHA_REG", "EMAIL_EST", "TELEFONO_EST", "DESCRIPCION_ESTADO"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, 'RECIÉN AGREGADO')
                RETURNING "ID_EST"
        """
        resultado = db_conector.ejecutar_consulta_unica(
            query_agregar_estudiante,
            (nombre, apellido, cedula, cedula_est, genero, estado, condicion, fecha_nac, email, telefono)
        )
        id_nuevo_estudiante = resultado.get("ID_EST")

        if not id_nuevo_estudiante:
            raise ValueError("No se pudo obtener el ID del nuevo estudiante. Verifica la inserción en la base de datos.")

        # Enlazar el estudiante con el representante
        if id_representante:
            query_vincular_padre = """
                INSERT INTO "REPRE_EST" ("ID_REPRE", "ID_EST", "ESTADO","FECHA_REG")
                VALUES (%s, %s, 'ACTIVO',NOW())
            """
            db_conector.ejecutar_modificacion(query_vincular_padre, (id_representante, id_nuevo_estudiante))

        return id_nuevo_estudiante

    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Error inesperado: {str(e)}"



def modificar_estudiante(id_estudiante, nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_cedula_est, 
                         nuevo_genero, nueva_condicion, nuevo_email, nuevo_telefono):
    """
    Modifica los datos generales de un estudiante en la base de datos.

    Args:
        id_estudiante (int): ID del estudiante a modificar.
        nuevo_nombre (str): Nuevo nombre del estudiante.
        nuevo_apellido (str): Nuevo apellido del estudiante.
        nueva_cedula (int): Nueva cédula del estudiante.
        nueva_cedula_est (int): Nueva cédula estudiantil.
        nuevo_genero (str): Nuevo género del estudiante ("varon" o "hembra").
        nueva_condicion (str): Nueva condición especial del estudiante.
        nuevo_email (str): Nuevo email del estudiante.
        nuevo_telefono (str): Nuevo teléfono del estudiante.

    Returns:
        bool: True si la modificación fue exitosa, False en caso contrario.
    """
    try:
        # Validación de género
        genero_normalizado = nuevo_genero.lower()
        if genero_normalizado not in ["varon", "hembra"]:
            raise ValueError("El género proporcionado no es válido. Debe ser 'varon' o 'hembra'.")

        # Validación de condición
        if not nueva_condicion or nueva_condicion.strip() == "":
            nueva_condicion = "no"

        # Actualizar datos del estudiante en la tabla "ESTUDIANTES"
        query_modificar_estudiante = """
            UPDATE "ESTUDIANTES"
            SET 
                "NOMBRE_EST" = %s, 
                "APELLIDO_EST" = %s, 
                "CEDULA" = %s, 
                "CEDULA_EST" = %s, 
                "GENERO" = %s, 
                "CONDICION" = %s,
                "EMAIL_EST" = %s,
                "TELEFONO_EST" = %s
            WHERE 
                "ID_EST" = %s
        """
        db_conector.ejecutar_modificacion(
            query_modificar_estudiante,
            (nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_cedula_est, 
             genero_normalizado, nueva_condicion, nuevo_email, nuevo_telefono, id_estudiante)
        )

        return True  # Operación exitosa

    except Exception as e:
        print(f"Error al modificar el estudiante: {e}")
        return False

def modificar_representante(id_estudiante, nuevo_id_representante, razon_cambio):
    """
    Modifica el representante de un estudiante y agrega un log del cambio realizado.

    Args:
        id_estudiante (int): ID del estudiante al que se le cambiará el representante.
        nuevo_id_representante (int): ID del nuevo representante.
        razon_cambio (str): Razón por la cual se cambia el representante.

    Returns:
        bool: True si el cambio fue exitoso, False en caso contrario.
    """
    try:
        # Recuperar la relación actual del estudiante (solo si el estado es "ACTIVO")
        query_verificar_representante = """
            SELECT "ID_REPRE", "ESTADO" FROM "REPRE_EST" WHERE "ID_EST" = %s AND "ESTADO" = 'ACTIVO'
        """
        resultado = db_conector.ejecutar_consulta_unica(query_verificar_representante, (id_estudiante,))
        id_representante_actual = resultado.get("ID_REPRE") if resultado else None
        estado_actual = resultado.get("ESTADO") if resultado else None

        # Si el representante es diferente y hay un representante actual con estado "ACTIVO", procedemos
        if id_representante_actual:
            # Cambiar el estado de la relación anterior a "ALTERADO"
            if id_representante_actual != nuevo_id_representante:
                query_modificar_estado_actual = """
                    UPDATE "REPRE_EST" 
                    SET "ESTADO" = 'ALTERADO'
                    WHERE "ID_EST" = %s AND "ID_REPRE" = %s
                """
                db_conector.ejecutar_modificacion(query_modificar_estado_actual, 
                                                   (id_estudiante, id_representante_actual))

        # Insertar la nueva relación con el nuevo representante y marcarla como "ACTIVO"
        query_insertar_nueva_relacion = """
            INSERT INTO "REPRE_EST" ("ID_REPRE", "ID_EST", "RAZON", "FECHA_CAMBIO", "CAMBIO_DE", "ESTADO")
            VALUES (%s, %s, %s, NOW(), %s, 'ACTIVO')
        """
        mensaje_cambio = f"Representante anterior (ID {id_representante_actual}) cambiado por nuevo representante (ID {nuevo_id_representante})"
        db_conector.ejecutar_modificacion(query_insertar_nueva_relacion, 
                                           (nuevo_id_representante, id_estudiante, razon_cambio, mensaje_cambio))

        return True  # Operación exitosa

    except Exception as e:
        print(f"Error al modificar el representante: {e}")
        return False





# Eliminar un estudiante
def eliminar_estudiante(id_est):
    try:
        # Eliminar relaciones en "REPRE_EST"
        query_eliminar_relacion = """
            DELETE FROM "REPRE_EST"
            WHERE "ID_EST" = %s
        """
        db_conector.ejecutar_modificacion(query_eliminar_relacion, (id_est,))

        # Eliminar el estudiante de la tabla "ESTUDIANTES"
        query_eliminar_estudiante = """
            DELETE FROM "ESTUDIANTES"
            WHERE "ID_EST" = %s
        """
        db_conector.ejecutar_modificacion(query_eliminar_estudiante, (id_est,))

    except Exception as e:
        print(f"Error al eliminar estudiante: {e}")
        raise

# Cambiar estado del estudiante
def cambiar_estado_estudiante(id_est, nuevo_estado, descripcion):
    try:
        query_cambiar_estado = """
            UPDATE "ESTUDIANTES"
            SET "ESTADO" = %s, "DESCRIPCION_ESTADO" = %s
            WHERE "ID_EST" = %s
        """
        db_conector.ejecutar_modificacion(query_cambiar_estado, (nuevo_estado, descripcion, id_est))

    except Exception as e:
        print(f"Error al cambiar estado del estudiante: {e}")
        raise

def guardar_imagen_estudiante(id_estudiante, imagen_estudiante):
    """
    Guarda la imagen del estudiante en la carpeta correspondiente dentro de Utilidades_db/PHOTO_EST.

    Parámetros:
    - id_estudiante (int): ID del estudiante.
    - imagen_estudiante (UploadedFile): Archivo de imagen subido en Streamlit.

    Retorna:
    - str: Mensaje de éxito o error.
    """
    try:
        if imagen_estudiante is not None:
            # Crear carpeta si no existe
            path = f"Utilidades_db/PHOTO_EST/{id_estudiante}"
            os.makedirs(path, exist_ok=True)  # Crea la carpeta si no existe

            # Definir la ruta del archivo
            imagen_path = os.path.join(path, f"Foto_{id_estudiante}.png")

            # Guardar la imagen
            image = Image.open(imagen_estudiante)
            image.save(imagen_path)

            return f"✅ Imagen guardada en {imagen_path}."
        else:
            return "⚠️ No se cargó ninguna imagen."
    except Exception as e:
        return f"❌ Error al guardar la imagen: {e}"
    


def obtener_historial_cambios_representantes(ids_estudiantes):
    # Si 'ids_estudiantes' es una Serie de pandas, conviértelo a una lista
    if isinstance(ids_estudiantes, pd.Series):
        ids_estudiantes = ids_estudiantes.tolist()  # Convertir a lista

    # Asegurarse de que `ids_estudiantes` sea una lista o tupla
    if not isinstance(ids_estudiantes, (list, tuple)):
        ids_estudiantes = [ids_estudiantes]  # Si es un solo ID, convertirlo a lista

    connection = db_conector.conectar()  # Conectar a la base de datos
    if connection:
        try:
            # Usar RealDictCursor para obtener resultados como diccionario
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            
            # Consultar los cambios de representantes para los estudiantes activos
            cursor.execute("""
SELECT 
    e."ID_EST", 
    e."NOMBRE_EST", 
    e."APELLIDO_EST", 
    r."NOMBRE_REP" AS "NOMBRE_REPRE", 
    r."APELLIDO_REP" AS "APELLIDO_REPRE", 
    re."ESTADO", 
    re."RAZON", 
    re."FECHA_CAMBIO", 
    re."CAMBIO_DE"
FROM 
    "REPRE_EST" re
JOIN 
    "ESTUDIANTES" e ON re."ID_EST" = e."ID_EST"
JOIN 
    "REPRESENTANTES" r ON re."ID_REPRE" = r."ID_REP"
WHERE 
    e."ID_EST" = ANY(%s)  -- Incluir tanto activos como inactivos
ORDER BY 
    re."FECHA_CAMBIO" DESC

            """, (ids_estudiantes,))  # Asegúrate de pasar la lista directamente

            # Obtener todos los resultados de la consulta
            historial_cambios = cursor.fetchall()
            return historial_cambios  # Devuelve la lista de diccionarios
        except psycopg2.OperationalError as e:  # Manejo de errores específico para psycopg2
            print(f"OperationalError al consultar historial de cambios: {e}")
            return None
        except psycopg2.Error as e:  # Manejo de otros errores de psycopg2
            print(f"Error al consultar historial de cambios: {e}")
            return None
        finally:
            db_conector.cerrar_conexion(connection)  # Asegúrate de cerrar la conexión



def obtener_asistencias_por_fecha_y_seccion(fecha_desde, fecha_hasta, seccion_seleccionada=None):
    """
    Obtiene las asistencias de los estudiantes dentro de un rango de fechas y una sección específica (opcional).
    :param fecha_desde: Fecha de inicio del rango
    :param fecha_hasta: Fecha de fin del rango
    :param seccion_seleccionada: Sección específica a filtrar (opcional)
    :return: Lista de registros de asistencias
    """
    try:
        # Asegurarse de que las fechas estén en formato de fecha (datetime.date)
        fecha_desde = fecha_desde.date() if isinstance(fecha_desde, datetime.datetime) else fecha_desde
        fecha_hasta = fecha_hasta.date() if isinstance(fecha_hasta, datetime.datetime) else fecha_hasta

        # Conectar a la base de datos
        connection = db_conector.conectar()

        # Crear el cursor
        cursor = connection.cursor()

        # Base de la consulta SQL
        query = """
SELECT 
    ae."ID_ASISTENCIA_ESTUD",
    e."NOMBRE_EST" AS "Nombre_Estudiante", 
    e."APELLIDO_EST" AS "Apellido_Estudiante",
    s."NOMBRE_SECCION" AS "Sección",
    g."NOMBRE_GRADO" AS "Grado",
    p."NOMBRE_PROF" || ' ' || p."APELLIDO_PROF" AS "Profesor_A_Cargo", 
    ae."FECHA_ASISTENCIA",
    ae."ESTADO_ASISTENCIA",
    ae."YEAR_ESCOLAR"
FROM 
    public."ASISTENCIA_ESTUDIANTES" ae
JOIN 
    public."ESTUDIANTES" e ON ae."ID_EST" = e."ID_EST"
JOIN 
    public."SECCIONES" s ON ae."ID_SECCION" = s."ID_SECCION"
JOIN 
    public."GRADOS" g ON s."ID_GRADO" = g."ID_GRADOS"
JOIN 
    public."PROFESORES" p ON s."ID_PROF" = p."ID_PROF"
WHERE 
    ae."FECHA_ASISTENCIA" BETWEEN %s AND %s
"""

        # Si se ha seleccionado una sección, agregar el filtro de sección a la consulta
        if seccion_seleccionada:
            query += " AND s.\"NOMBRE_SECCION\" = %s"
            cursor.execute(query, (fecha_desde, fecha_hasta, seccion_seleccionada))
        else:
            cursor.execute(query, (fecha_desde, fecha_hasta))

        # Obtener los resultados
        asistencias = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return asistencias

    except Exception as e:
        print(f"Error al obtener asistencias: {e}")
        return None



def obtener_grados():
    """
    Obtiene la lista de grados desde la base de datos.
    """
    conn = db_conector.conectar()
    cursor = conn.cursor()
    query = 'SELECT "ID_GRADOS", "NOMBRE_GRADO" FROM "GRADOS";'
    cursor.execute(query)
    grados = cursor.fetchall()
    cursor.close()
    conn.close()
    return grados  # Retorna la lista de tuplas (ID_GRADOS, NOMBRE_GRADO)



def obtener_secciones_por_grado(grado_seleccionado):
    """
    Obtiene las secciones para un grado específico desde la base de datos.
    """
    conn = db_conector.conectar()
    cursor = conn.cursor()
    
    # La consulta puede estar filtrando por grado
    query = '''SELECT s."ID_SECCION", s."NOMBRE_SECCION", g."NOMBRE_GRADO", p."NOMBRE_PROF", p."APELLIDO_PROF"
               FROM "SECCIONES" s
               JOIN "GRADOS" g ON s."ID_GRADO" = g."ID_GRADOS"
               JOIN "PROFESORES" p ON s."ID_PROF" = p."ID_PROF"
               WHERE g."NOMBRE_GRADO" = %s;'''
    cursor.execute(query, (grado_seleccionado,))
    secciones = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return secciones
