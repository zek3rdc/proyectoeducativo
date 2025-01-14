from modulos import db_conector
import pandas as pd
import datetime

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
def agregar_estudiante(nombre, apellido, cedula, cedula_est, id_representante, genero, estado, descripcion_estado, fecha_nac, email, telefono):
    try:
        # Validar si la cédula ya existe
        if db_conector.cedula_existe(cedula):
            return f"La cédula {cedula} ya está registrada en la base de datos."

        # Validar si la matrícula ya existe
        if db_conector.matricula_existe(cedula_est):
            return f"La matrícula {cedula_est} ya está registrada en la base de datos."

        # Establecer la condición predeterminada como "NO" si está vacía
        if not descripcion_estado:
            descripcion_estado = "NO"

        # Insertar el estudiante
        query_agregar_estudiante = """
            INSERT INTO "ESTUDIANTES" (
                "NOMBRE_EST", "APELLIDO_EST", "CEDULA", "CEDULA_EST", 
                "GENERO", "ESTADO", "CONDICION", "FECHA_NAC", 
                "FECHA_REG", "EMAIL_EST", "TELEFONO_EST"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s)
            RETURNING "ID_EST"
        """
        resultado = db_conector.ejecutar_consulta_unica(
            query_agregar_estudiante,
            (nombre, apellido, cedula, cedula_est, genero, estado, descripcion_estado, fecha_nac, email, telefono)
        )
        id_nuevo_estudiante = resultado.get("ID_EST")

        if not id_nuevo_estudiante:
            raise ValueError("No se pudo obtener el ID del nuevo estudiante. Verifica la inserción en la base de datos.")

        # Enlazar el estudiante con el representante
        if id_representante:
            query_vincular_padre = """
                INSERT INTO "REPRE_EST" ("ID_REPRE", "ID_EST")
                VALUES (%s, %s)
            """
            db_conector.ejecutar_modificacion(query_vincular_padre, (id_representante, id_nuevo_estudiante))

        return id_nuevo_estudiante

    except ValueError as ve:
        # Manejar errores específicos
        return str(ve)
    except Exception as e:
        # Manejar errores generales
        return f"Error inesperado: {str(e)}"


# Modificar un estudiante
def modificar_estudiante(id_estudiante, nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_cedula_est, nuevo_genero, nueva_condicion,nuevo_email,nuevo_telefono):
    """
    Modifica los datos de un estudiante en la base de datos.

    Args:
        id_est (int): ID del estudiante a modificar.
        nuevo_nombre (str): Nuevo nombre del estudiante.
        nuevo_apellido (str): Nuevo apellido del estudiante.
        nueva_cedula (int): Nueva cédula del estudiante.
        nueva_cedula_est (int): Nueva cédula estudiantil.
        nuevo_genero (str): Nuevo género del estudiante ("varon" o "hembra").
        nuevo_estado (str): Nuevo estado del estudiante ("Activo" o "Inactivo").
        nueva_condicion (str): Nueva condición especial del estudiante.

    Returns:
        bool: True si la modificación fue exitosa, False en caso contrario.
    """
    try:
        # Validación de género
        genero_normalizado = nuevo_genero.lower()
        if genero_normalizado not in ["varon", "hembra"]:
            raise ValueError("El género proporcionado no es válido. Debe ser 'varon' o 'hembra'.")

        # Validación de estado


        # Consulta SQL para actualizar el estudiante
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

        # Ejecutar la modificación en la base de datos
        db_conector.ejecutar_modificacion(
            query_modificar_estudiante,
            (nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_cedula_est, 
             genero_normalizado, nueva_condicion,nuevo_email,nuevo_telefono, id_estudiante)
        )

        return True  # Operación exitosa

    except ValueError as ve:
        print(f"Validación fallida: {ve}")
        return False  # Error en los datos proporcionados
    except Exception as e:
        print(f"Error al modificar estudiante: {e}")
        return False  # Error en la operación

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
