from modulos.db_conector import ejecutar_query, ejecutar_consulta_unica

def obtener_representantes():
    query = 'SELECT * FROM "REPRESENTANTES";'
    return ejecutar_query(query, fetch_all=True)

def agregar_representante(nombre, apellido, cedula, telefono_principal, direccion, fecha_nac, telefonos_adicionales=""):
    try:
        # Primero insertar el representante
        query_insertar_representante = """
            INSERT INTO "REPRESENTANTES" ("NOMBRE_REP", "APELLIDO_REP", "CEDULA_REP", "DIRECCION_REP","TELEFONO_REP", "FECHA_NAC_REP", "FECHA_REG_REP")
            VALUES (%s, %s, %s, %s, %s, %s, NOW()) RETURNING "ID_REP";
        """
        parametros = (nombre, apellido, cedula, direccion, telefono_principal, fecha_nac)
        resultado = ejecutar_consulta_unica(query_insertar_representante, parametros=parametros)
        
        # Verificar si el ID_REP fue devuelto correctamente
        if not resultado or "ID_REP" not in resultado:
            raise ValueError("No se pudo obtener el ID del representante después de la inserción.")
        
        id_rep = resultado["ID_REP"]
        
        # Verificar que el representante se haya insertado correctamente
        query_verificar_representante = '''SELECT 1 FROM "REPRESENTANTES" WHERE "ID_REP" = %s'''
        verificacion = ejecutar_query(query_verificar_representante, parametros=(id_rep,), fetch_all=False)
        
        if not verificacion:
            raise ValueError(f"El representante con ID {id_rep} no se encuentra en la base de datos.")
        
        # Ahora agregar el teléfono principal
        agregar_telefono(id_rep, telefono_principal)

        # Agregar teléfonos adicionales, si existen
        if telefonos_adicionales:
            for telefono in telefonos_adicionales.split(","):
                telefono = telefono.strip()
                if telefono:
                    agregar_telefono(id_rep, telefono)
        
        return {"ID_REP": id_rep}
    
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}


def agregar_telefono(id_rep, telefono):
    # Verificar si el ID_REP existe en la tabla REPRESENTANTES
    query_check = 'SELECT 1 FROM "REPRESENTANTES" WHERE "ID_REP" = %s;'
    check_result = ejecutar_query(query_check, parametros=(id_rep,), fetch_all=False)
    
    if check_result:
        query = 'INSERT INTO "TELEFONOS_REPRE" ("ID_REP", "TELEFONO", "FECHA_REG") VALUES (%s, %s, NOW());'
        return ejecutar_query(query, parametros=(id_rep, telefono))
    else:
        raise ValueError(f"El ID_REP {id_rep} no existe en la tabla REPRESENTANTES.")


def eliminar_representante(id_rep):
    query = 'DELETE FROM "REPRESENTANTES" WHERE "ID_REP" = %s;'
    return ejecutar_query(query, parametros=(id_rep,))

def actualizar_representante(id_rep, nombre, apellido, cedula, telefono, direccion):
    query = '''
    UPDATE "REPRESENTANTES"
    SET "NOMBRE_REP" = %s, "APELLIDO_REP" = %s, "CEDULA_REP" = %s, "TELEFONO_REP" = %s, "DIRECCION_REP" = %s
    WHERE "ID_REP" = %s;
    '''
    return ejecutar_query(query, parametros=(nombre, apellido, cedula, telefono, direccion, id_rep))


def obtener_telefonos_representante(id_rep):
    try:
        # Ejecutar la consulta para obtener los teléfonos
        query = 'SELECT "TELEFONO" FROM "TELEFONOS_REPRE" WHERE "ID_REP" = %s;'
        resultados = ejecutar_query(query, parametros=(id_rep,), fetch_all=True)

        # Si la consulta devuelve resultados, extraemos los teléfonos
        if resultados:
            return [r["TELEFONO"] for r in resultados]
        else:
            return []  # Si no hay resultados, retornamos una lista vacía

    except Exception as e:
        # Manejo de errores, por si algo falla en la ejecución de la consulta
        return {"error": f"Error al obtener los teléfonos: {str(e)}"}



def eliminar_telefonos_representante(id_rep):
    query = 'DELETE FROM "TELEFONOS_REPRE" WHERE "ID_REP" = %s;'
    return ejecutar_query(query, parametros=(id_rep,))
