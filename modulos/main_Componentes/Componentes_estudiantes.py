from modulos import db_conector
import pandas as pd

def renombrar_columnas(df):
    return df.rename(columns={
        'ID_EST': 'ID Estudiante',
        'nombre_est': 'Nombre',
        'apellido_est': 'Apellido',
        'matricula': 'Matrícula',
        'ci_est': 'Cédula Estudiantil',
        'estado': 'Estado',
        'razon': 'Razón',
        'genero': 'Género',
        'id_padre': 'ID Padre',
        'nombre_repre': 'Nombre Padre',
        'apellido_repre': 'Apellido Padre',
        'cedula_repre': 'Cédula Padre'
    })

def agregar_estudiante(nombre, apellido, matricula, cedula, id_padre, genero):
    # Consulta para agregar el estudiante
    query_agregar_estudiante = """
        INSERT INTO estudiantes (NOMBRE_EST, APELLIDO_ESt, CEDULA, CEDULA_EST, GENERO)
        VALUES (%s, %s, %s, %s, %s)
    """
    db_conector.ejecutar_modificacion(query_agregar_estudiante, (nombre, apellido, matricula, cedula, genero))
    
    # Obtener el ID del último estudiante agregado
    id_nuevo_estudiante = db_conector.obtener_ultimo_ID_EST()

    # Consulta para enlazar el estudiante con el padre en padres_estudiantes
    query_vincular_padre = """
        INSERT INTO padres_estudiantes (ID_EST, ID_REP)
        VALUES (%s, %s)
    """
    db_conector.ejecutar_modificacion(query_vincular_padre, (id_nuevo_estudiante, id_padre))
    
    return id_nuevo_estudiante

def modificar_estudiante(est_data, nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula):
    query_modificar_estudiante = """
        UPDATE estudiantes
        SET NOMBRE_EST = %s, APELLIDO_EST = %s, CEDULA = %s, CEDULA_EST = %s
        where ID_EST = %s
    """
    db_conector.ejecutar_modificacion(query_modificar_estudiante, (nuevo_nombre, nuevo_apellido, nueva_matricula, nueva_cedula, est_data['ID_EST']))

def eliminar_estudiante(ID_EST):
    # Consulta para eliminar las relaciones en la tabla padres_estudiantes
    query_eliminar_relacion = """
        DELETE FROM REPRE_EST
        WHERE ID_EST = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_relacion, (ID_EST,))

    # Consulta para eliminar el estudiante de la tabla estudiantes
    query_eliminar_estudiante = """
        DELETE FROM ESTUDIANTES
        WHERE ID_EST = %s
    """
    db_conector.ejecutar_modificacion(query_eliminar_estudiante, (ID_EST,))

def cambiar_estado_estudiante(est_id, nuevo_estado, descripcion):
    query_cambiar_estado = """
        UPDATE ESTUDIANTES
        set ESTADO = %s, DESCRIPCION = %s
        where ID_EST = %s
    """
    db_conector.ejecutar_modificacion(query_cambiar_estado, (nuevo_estado, descripcion, est_id))
