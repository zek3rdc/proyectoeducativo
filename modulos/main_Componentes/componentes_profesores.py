from modulos import db_conector

def agregar_profesor(nombre, apellido, fecha_nac,cedula, email, telefono, direccion, codificacion,categoria,estudios,fecha_job, rol):
    """
    Agrega un nuevo profesor a la base de datos.
    """
    # Obtener el ID del rol a partir del nombre del rol
    query_rol = '''
        SELECT "ID_ROL" FROM public."ROLES" WHERE "ROL" = %s;
    '''
    rol_id = db_conector.ejecutar_query(query_rol, (rol,))[0]["ID_ROL"]
    
    query = '''
        INSERT INTO public."PROFESORES" (
            "NOMBRE_PROF", 
            "APELLIDO_PROF",
            "FECHA_NAC_PERSONAL",
            "CEDULA_PROF", 
            "EMAIL_PROF", 
            "TELEFONO_PROF", 
            "DIRECCION_PROF",
            "CODIFICACION",
            "CATEGORIA",
            "ESTUDIOS_ACTUAL",
            "FECHA_LABORAL", 
            "ID_ROL",
            "FECHA_REG_PROF"
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,NOW());
    '''
    db_conector.ejecutar_query(query, (nombre, apellido, fecha_nac,cedula, email, telefono, direccion, codificacion,categoria,estudios,fecha_job, rol_id))


def editar_profesor(id_profesor, nombre, apellido,fecha_nac, cedula, email, telefono, direccion,codificacion,categoria,estudios,fecha_job, rol):
    """
    Actualiza los datos de un profesor en la base de datos.
    """
    # Obtener el ID del rol a partir del nombre del rol
    query_rol = '''
        SELECT "ID_ROL" FROM public."ROLES" WHERE "ROL" = %s;
    '''
    rol_id = db_conector.ejecutar_query(query_rol, (rol,))[0]["ID_ROL"]
    
    query = '''
        UPDATE public."PROFESORES"
        SET 
            "NOMBRE_PROF" = %s,
            "APELLIDO_PROF" = %s,
            "FECHA_NAC_PERSONAL" = %s,
            "CEDULA_PROF" = %s,
            "EMAIL_PROF" = %s,
            "TELEFONO_PROF" = %s,
            "DIRECCION_PROF" = %s,
            "CODIFICACION" = %s,
            "CATEGORIA" = %s,
            "ESTUDIOS_ACTUAL" = %s,
            "FECHA_LABORAL" = %s,
            "ID_ROL" = %s
        WHERE "ID_PROF" = %s;
    '''
    db_conector.ejecutar_query(query, ( nombre, apellido,fecha_nac, cedula, email, telefono, direccion,codificacion,categoria,estudios,fecha_job, rol_id, id_profesor))

def eliminar_profesor(id_profesor):
    """
    Elimina un profesor de la base de datos.
    """
    query = '''
        DELETE FROM public."PROFESORES"
        WHERE "ID_PROF" = %s;
    '''
    db_conector.ejecutar_query(query, (id_profesor,))



def listar_roles():
    """
    Obtiene la lista de roles desde la base de datos.
    """
    query = '''
        SELECT "ROL" FROM public."ROLES";
    '''
    resultados = db_conector.ejecutar_query(query)
    
    # Extraemos solo los valores de la columna "ROL" para usar en el selectbox
    roles = [row["ROL"] for row in resultados]
    return roles

def agregar_rol(rol):
    """
    Inserta un nuevo rol en la base de datos en la tabla "ROLES".
    """
    query = "INSERT INTO public.\"ROLES\" (\"ROL\") VALUES (%s);"
    db_conector.ejecutar_query(query, (rol,))

def editar_rol(rol_actual, nuevo_rol):
    """
    Actualiza el nombre de un rol en la tabla "ROLES".
    """
    query = '''
    UPDATE public."ROLES"
    SET "ROL" = %s
    WHERE "ROL" = %s;
    '''
    try:
        db_conector.ejecutar_query(query, (nuevo_rol, rol_actual))
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        raise

def eliminar_rol(rol):
    """
    Elimina un rol de la base de datos en la tabla "ROLES".
    """
    query = "DELETE FROM public.\"ROLES\" WHERE \"ROL\" = %s;"
    db_conector.ejecutar_query(query, (rol,))
