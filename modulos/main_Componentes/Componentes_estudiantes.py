from modulos import db_conector


def agregar_estudiante(nombre, apellido, matricula, cedula, id_padre, genero):
    # Consulta para agregar el estudiante
    query_agregar_estudiante = """
        INSERT INTO estudiantes (nombre, apellido, matricula, Cedula, Genero, id_clase)
        VALUES (%s, %s, %s, %s, %s, 1)
    """
    db_conector.ejecutar_modificacion(query_agregar_estudiante, (nombre, apellido, matricula, cedula, genero))
    
    # Obtener el ID del último estudiante agregado
    id_nuevo_estudiante = db_conector.obtener_ultimo_id_estudiante()

    # Consulta para enlazar el estudiante con el padre en padres_estudiantes
    query_vincular_padre = """
        INSERT INTO padres_estudiantes (id_estudiante, id_padres)
        VALUES (%s, %s)
    """
    db_conector.ejecutar_modificacion(query_vincular_padre, (id_nuevo_estudiante, id_padre))  # Aquí asegurarte de pasar solo los parámetros requeridos
    
    return id_nuevo_estudiante


def modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula):
    query_modificar_estudiante = """
        UPDATE estudiantes
        SET nombre = %s, apellido = %s, matricula = %s, Cedula = %s
        WHERE id_estudiante = %s
    """
    db_conector.ejecutar_modificacion(query_modificar_estudiante, (nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula, est_data['id_estudiante']))

def eliminar_estudiante(id_estudiante):
    # Consulta para eliminar las relaciones en la tabla padres_estudiantes
    query_eliminar_relacion = """
        DELETE FROM padres_estudiantes
        WHERE id_estudiante = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_relacion, (id_estudiante,))

    # Consulta para eliminar el estudiante de la tabla estudiantes
    query_eliminar_estudiante = """
        DELETE FROM estudiantes
        WHERE id_estudiante = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_estudiante, (id_estudiante,))


def cambiar_estado_estudiante(est_id, nuevo_estado, descripcion):
    db_conector.cambiar_estado_estudiante(est_id, nuevo_estado, descripcion)
