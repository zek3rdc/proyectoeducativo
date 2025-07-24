from modulos import db_conector
import pandas as pd
import datetime

# Importar modelos necesarios
from models import Grados, Secciones, Profesores, Estudiantes, AsignacionEst, AsistenciaEstudiantes, AsistenciaProfesores

def obtener_secciones(user_id):
    """Obtiene las secciones asignadas al usuario (profesor)."""
    with db_conector.get_db() as db:
        try:
            secciones_data = db.query(
                Grados.ID_GRADOS,
                Grados.NOMBRE_GRADO,
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION
            ).join(Secciones, Grados.ID_GRADOS == Secciones.ID_GRADO)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .filter(Profesores.ID_ACCESO == user_id).distinct().all()
            
            return [row._asdict() for row in secciones_data]
        except Exception as e:
            print(f"Error al obtener secciones: {e}")
            return []

def obtener_estudiantes(user_id):
    """Obtiene los estudiantes asignados al usuario (profesor)."""
    with db_conector.get_db() as db:
        try:
            estudiantes_data = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Estudiantes.CEDULA_EST,
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION
            ).join(AsignacionEst, Estudiantes.ID_EST == AsignacionEst.ID_EST)\
            .join(Secciones, AsignacionEst.ID_SECCION == Secciones.ID_SECCION)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .filter(Profesores.ID_ACCESO == user_id).all()
            
            return [row._asdict() for row in estudiantes_data]
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []

def registrar_asistencia_estudiante(id_estudiante, id_seccion, fecha_asistencia, asistio, justificacion=False):
    """Registra o actualiza la asistencia de un estudiante en una sección, incluyendo la justificación."""
    today = datetime.date.today()
    year_escolar = f"{today.year}-09-01" if today.month >= 9 else f"{today.year-1}-09-01"

    with db_conector.get_db() as db:
        try:
            # Verificar si la asistencia ya existe
            asistencia_existente = db.query(AsistenciaEstudiantes).filter(
                AsistenciaEstudiantes.ID_EST == id_estudiante,
                AsistenciaEstudiantes.FECHA_ASISTENCIA == fecha_asistencia
            ).first()

            if asistencia_existente:
                # Si la asistencia ya existe, actualizar el estado y la justificación
                asistencia_existente.ESTADO_ASISTENCIA = asistio
                asistencia_existente.JUSTIFICACION = justificacion
                db.add(asistencia_existente)
            else:
                # Si la asistencia no existe, insertar un nuevo registro
                nueva_asistencia = AsistenciaEstudiantes(
                    ID_EST=id_estudiante,
                    ID_SECCION=id_seccion,
                    FECHA_ASISTENCIA=fecha_asistencia,
                    ESTADO_ASISTENCIA=asistio,
                    JUSTIFICACION=justificacion,
                    YEAR_ESCOLAR=year_escolar
                )
                db.add(nueva_asistencia)
            
            db.commit()
            return True # O el objeto de asistencia si se necesita
        except Exception as e:
            db.rollback()
            print(f"Error al registrar/actualizar asistencia de estudiante: {e}")
            return False

def registrar_asistencia_profesor(user_id, seccion_id): # Cambiado 'seccion' a 'seccion_id' para claridad
    """Registra la asistencia del profesor a una sección."""
    with db_conector.get_db() as db:
        try:
            profesor = db.query(Profesores).filter(Profesores.ID_ACCESO == user_id).first()
            if not profesor:
                print(f"Profesor con ID_ACCESO {user_id} no encontrado.")
                return False
            
            # Verificar si ya existe un registro de asistencia para hoy para este profesor
            asistencia_existente = db.query(AsistenciaProfesores).filter(
                AsistenciaProfesores.ID_PROF == profesor.ID_PROF,
                AsistenciaProfesores.FECHA_ASISTENCIA == datetime.date.today()
            ).first()

            if asistencia_existente:
                print(f"Asistencia del profesor {profesor.NOMBRE_PROF} ya registrada para hoy.")
                return False # O actualizar si es el comportamiento deseado

            # Insertar nueva asistencia
            nueva_asistencia_prof = AsistenciaProfesores(
                ID_PROF=profesor.ID_PROF,
                FECHA_ASISTENCIA=datetime.date.today(),
                ESTADO_ASISTENCIA=True,
                YEAR_ESCOLAR=str(datetime.date.today().year) # Asumiendo que YEAR_ESCOLAR es un string
            )
            db.add(nueva_asistencia_prof)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al registrar asistencia de profesor: {e}")
            return False

def obtener_asistencias_estudiantes(seccion_id, fecha_inicio=None, fecha_fin=None):
    """Obtiene las asistencias de los estudiantes en una sección, con opción de filtrar por rango de fechas."""
    with db_conector.get_db() as db:
        try:
            query = db.query(
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                AsistenciaEstudiantes.FECHA_ASISTENCIA,
                AsistenciaEstudiantes.ESTADO_ASISTENCIA,
                AsistenciaEstudiantes.JUSTIFICACION,
                Estudiantes.ID_EST
            ).join(Estudiantes, AsistenciaEstudiantes.ID_EST == Estudiantes.ID_EST)\
            .join(Secciones, AsistenciaEstudiantes.ID_SECCION == Secciones.ID_SECCION)\
            .filter(AsistenciaEstudiantes.ID_SECCION == seccion_id)

            if fecha_inicio and fecha_fin:
                query = query.filter(AsistenciaEstudiantes.FECHA_ASISTENCIA.between(fecha_inicio, fecha_fin))
            
            asistencias = query.all()
            return pd.DataFrame([row._asdict() for row in asistencias])
        except Exception as e:
            print(f"Error al obtener asistencias de estudiantes: {e}")
            return pd.DataFrame()

def modificar_asistencia_estudiante(estudiante_nombre_completo, seccion_nombre, nuevo_estado):
    """Modifica el estado de asistencia de un estudiante en una sección."""
    nombre, apellido = estudiante_nombre_completo.split(" ", 1)
    
    with db_conector.get_db() as db:
        try:
            estudiante = db.query(Estudiantes).filter(
                Estudiantes.NOMBRE_EST == nombre,
                Estudiantes.APELLIDO_EST == apellido
            ).first()
            
            seccion = db.query(Secciones).filter(Secciones.NOMBRE_SECCION == seccion_nombre).first()

            if not estudiante or not seccion:
                print("Estudiante o Sección no encontrados.")
                return False

            asistencia = db.query(AsistenciaEstudiantes).filter(
                AsistenciaEstudiantes.ID_EST == estudiante.ID_EST,
                AsistenciaEstudiantes.ID_SECCION == seccion.ID_SECCION,
                AsistenciaEstudiantes.FECHA_ASISTENCIA == datetime.date.today()
            ).first()

            if asistencia:
                asistencia.ESTADO_ASISTENCIA = nuevo_estado
                db.add(asistencia)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al modificar asistencia de estudiante: {e}")
            return False

def eliminar_asistencia_por_estudiante_y_fecha(id_estudiante, fecha_asistencia):
    """Elimina el registro de asistencia de un estudiante en una fecha específica."""
    with db_conector.get_db() as db:
        try:
            asistencia = db.query(AsistenciaEstudiantes).filter(
                AsistenciaEstudiantes.ID_EST == id_estudiante,
                AsistenciaEstudiantes.FECHA_ASISTENCIA == fecha_asistencia
            ).first()
            
            if asistencia:
                db.delete(asistencia)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar asistencia: {e}")
            return False

def obtener_todas_las_secciones():
    with db_conector.get_db() as db:
        try:
            secciones_data = db.query(
                Grados.ID_GRADOS,
                Grados.NOMBRE_GRADO,
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION
            ).join(Secciones, Grados.ID_GRADOS == Secciones.ID_GRADO)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF).distinct().all()
            
            return [row._asdict() for row in secciones_data]
        except Exception as e:
            print(f"Error al obtener todas las secciones: {e}")
            return []

def obtener_todos_los_estudiantes():
    """Obtiene todos los estudiantes registrados con su ID_SECCION."""
    with db_conector.get_db() as db:
        try:
            estudiantes_data = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Estudiantes.CEDULA_EST,
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION
            ).join(AsignacionEst, Estudiantes.ID_EST == AsignacionEst.ID_EST)\
            .join(Secciones, AsignacionEst.ID_SECCION == Secciones.ID_SECCION).all()
            
            return [row._asdict() for row in estudiantes_data]
        except Exception as e:
            print(f"Error al obtener todos los estudiantes: {e}")
            return []
