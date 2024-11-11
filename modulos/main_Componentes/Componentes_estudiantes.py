from modulos import db_conector
import pandas as pd

def renombrar_columnas(df):
    return df.rename(columns={
        'ID_ESTUDIANTE': 'ID Estudiante',
        'NOMBRE_EST': 'Nombre',
        'APELLIDO_EST': 'Apellido',
        'MATRICULA': 'Matrícula',
        'CI_EST': 'Cédula Estudiantil',
        'ESTADO': 'Estado',
        'RAZON': 'Razón',
        'GENERO': 'Género',
        'ID_PADRE': 'ID Padre',
        'NOMBRE_REPRE': 'Nombre Padre',
        'APELLIDO_REPRE': 'Apellido Padre',
        'CEDULA_REPRE': 'Cédula Padre'
    })

def agregar_estudiante(nombre, apellido, matricula, cedula, id_padre, genero):
    # Consulta para agregar el estudiante
    query_agregar_estudiante = """
        INSERT INTO estudiantes (NOMBRE_EST, APELLIDO_EST, CI_EST, CEDULA_EST, GENERO)
        VALUES (%s, %s, %s, %s, %s)
    """
    db_conector.ejecutar_modificacion(query_agregar_estudiante, (nombre, apellido, matricula, cedula, genero))
    
    # Obtener el ID del último estudiante agregado
    id_nuevo_estudiante = db_conector.obtener_ultimo_id_estudiante()

    # Consulta para enlazar el estudiante con el padre en padres_estudiantes
    query_vincular_padre = """
        INSERT INTO padres_estudiantes (ID_ESTUDIANTES, ID_REPRESENTANTES)
        VALUES (%s, %s)
    """
    db_conector.ejecutar_modificacion(query_vincular_padre, (id_nuevo_estudiante, id_padre))
    
    return id_nuevo_estudiante

def modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula):
    query_modificar_estudiante = """
        UPDATE estudiantes
        SET NOMBRE_EST = %s, APELLIDO_EST = %s, MATRICULA = %s, CI_EST = %s
        WHERE ID_ESTUDIANTE = %s
    """
    db_conector.ejecutar_modificacion(query_modificar_estudiante, (nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula, est_data['ID_ESTUDIANTE']))

def eliminar_estudiante(id_estudiante):
    # Consulta para eliminar las relaciones en la tabla padres_estudiantes
    query_eliminar_relacion = """
        DELETE FROM padres_estudiantes
        WHERE ID_ESTUDIANTES = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_relacion, (id_estudiante,))

    # Consulta para eliminar el estudiante de la tabla estudiantes
    query_eliminar_estudiante = """
        DELETE FROM estudiantes
        WHERE ID_ESTUDIANTE = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_estudiante, (id_estudiante,))

def cambiar_estado_estudiante(est_id, nuevo_estado, descripcion):
    query_cambiar_estado = """
        UPDATE estudiantes
        SET ESTADO = %s, DESCRIPCION = %s
        WHERE ID_ESTUDIANTE = %s
    """
    db_conector.ejecutar_modificacion(query_cambiar_estado, (nuevo_estado, descripcion, est_id))
