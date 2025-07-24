from modulos.db_conector import get_db # Importar get_db directamente
import pandas as pd
import datetime # Necesario para el año escolar

# Importar modelos necesarios
from models import Roles, Profesores, AsistenciaProfesores

def obtener_roles():
    with get_db() as db:
        try:
            roles = db.query(Roles.ID_ROL, Roles.ROL).all()
            return {rol.ID_ROL: rol.ROL for rol in roles}
        except Exception as e:
            print(f"Error al obtener roles: {e}")
            return {}

def obtener_personal():
    with get_db() as db:
        try:
            personal_data = db.query(
                Profesores.ID_PROF.label('ID_PERSONAL'),
                Profesores.NOMBRE_PROF.label('NOMBRE_PERSONAL'),
                Profesores.APELLIDO_PROF.label('APELLIDO_PERSONAL'),
                Profesores.CEDULA_PROF.label('CEDULA_PERSONAL'),
                Profesores.ID_ROL,
                Roles.ROL
            ).join(Roles, Profesores.ID_ROL == Roles.ID_ROL).all()
            
            return [p._asdict() for p in personal_data]
        except Exception as e:
            print(f"Error al obtener personal: {e}")
            return []

def registrar_asistencia_personal(id_personal, fecha_asistencia, asistio, justificacion):
    with get_db() as db:
        try:
            year_escolar = str(fecha_asistencia.year) # Convertir a string si es necesario
            
            nueva_asistencia = AsistenciaProfesores(
                ID_PROF=id_personal,
                FECHA_ASISTENCIA=fecha_asistencia,
                ESTADO_ASISTENCIA=asistio,
                JUSTIFICACION=justificacion,
                YEAR_ESCOLAR=year_escolar
            )
            db.add(nueva_asistencia)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al registrar asistencia: {e}")
            return False

def obtener_asistencias_personal(id_personal, fecha_inicio, fecha_fin):
    with get_db() as db:
        try:
            asistencias = db.query(
                AsistenciaProfesores.FECHA_ASISTENCIA.label("Fecha"),
                AsistenciaProfesores.ESTADO_ASISTENCIA.label("Asistió"),
                AsistenciaProfesores.JUSTIFICACION.label("Justificación")
            ).filter(
                AsistenciaProfesores.ID_PROF == id_personal,
                AsistenciaProfesores.FECHA_ASISTENCIA.between(fecha_inicio, fecha_fin)
            ).all()
            
            return pd.DataFrame([a._asdict() for a in asistencias])
        except Exception as e:
            print(f"Error al obtener asistencias: {e}")
            return pd.DataFrame()

def modificar_asistencia_personal(id_personal, fecha_asistencia, estado_asistencia, justificacion):
    """Modifica el estado de asistencia y justificación de un profesor en una fecha específica."""
    with get_db() as db:
        try:
            asistencia = db.query(AsistenciaProfesores).filter(
                AsistenciaProfesores.ID_PROF == id_personal,
                AsistenciaProfesores.FECHA_ASISTENCIA == fecha_asistencia
            ).first()
            
            if asistencia:
                asistencia.ESTADO_ASISTENCIA = estado_asistencia
                asistencia.JUSTIFICACION = justificacion
                db.add(asistencia)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al modificar asistencia: {e}")
            return False

def obtener_asistencias_por_rol(id_rol, fecha_inicio, fecha_fin):
    """
    Obtiene las asistencias de los profesores asociados a un rol dentro de un rango de fechas.
    """
    with get_db() as db:
        try:
            asistencias_data = db.query(
                AsistenciaProfesores.ID_PROF,
                Profesores.NOMBRE_PROF,
                Profesores.APELLIDO_PROF,
                AsistenciaProfesores.FECHA_ASISTENCIA,
                AsistenciaProfesores.ESTADO_ASISTENCIA,
                AsistenciaProfesores.JUSTIFICACION
            ).join(Profesores, AsistenciaProfesores.ID_PROF == Profesores.ID_PROF)\
            .filter(
                Profesores.ID_ROL == id_rol,
                AsistenciaProfesores.FECHA_ASISTENCIA.between(fecha_inicio, fecha_fin)
            ).all()
            
            return pd.DataFrame([row._asdict() for row in asistencias_data])
        except Exception as e:
            print(f"Error al obtener asistencias por rol: {e}")
            return pd.DataFrame()
    
def actualizar_asistencia_profesor(id_prof, fecha_asistencia, estado_asistencia, justificacion):
    """
    Actualiza el estado de asistencia y justificación de un profesor en una fecha específica.
    """
    return modificar_asistencia_personal(id_prof, fecha_asistencia, estado_asistencia, justificacion)
