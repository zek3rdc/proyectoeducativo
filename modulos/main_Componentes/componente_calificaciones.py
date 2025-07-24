from modulos import db_conector
import streamlit as st

# Importar modelos necesarios
from models import Secciones, Grados, Profesores, Calificaciones, Estudiantes, Materias

# Función para obtener las secciones y calificaciones asignadas al profesor
def obtener_datos_calificaciones(id_acceso):
    with db_conector.get_db() as db:
        try:
            # Obtener el ID_PROF del profesor usando ID_ACCESO
            profesor = db.query(Profesores).filter(Profesores.ID_ACCESO == id_acceso).first()
            if not profesor:
                st.error("Profesor no encontrado.")
                return None, None
            
            profesor_id = profesor.ID_PROF

            # Obtener secciones asignadas al profesor
            secciones_data = db.query(
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION,
                Grados.NOMBRE_GRADO
            ).join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
            .filter(Secciones.ID_PROF == profesor_id).all()
            
            secciones = [s._asdict() for s in secciones_data]

            # Obtener calificaciones para las secciones del profesor
            # Primero, obtener los IDs de las secciones para el filtro IN
            seccion_ids = [s.ID_SECCION for s in secciones_data]

            calificaciones_data = db.query(
                Calificaciones.ID_CALIFICACION,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Materias.NOMBRE_MATERIA,
                Calificaciones.CALIFICACION,
                Calificaciones.FECHA_CALIFICACION,
                Secciones.NOMBRE_SECCION
            ).join(Estudiantes, Calificaciones.ID_EST == Estudiantes.ID_EST)\
            .join(Materias, Calificaciones.ID_MATERIA == Materias.ID_MATERIA)\
            .join(Secciones, Calificaciones.ID_SECCION == Secciones.ID_SECCION)\
            .filter(Calificaciones.ID_SECCION.in_(seccion_ids)).all()
            
            calificaciones = [c._asdict() for c in calificaciones_data]

            return secciones, calificaciones
        except Exception as e:
            st.error(f"Error al obtener datos: {e}")
            return None, None

# Función para actualizar calificaciones en la base de datos
def actualizar_calificacion(id_calificacion, nueva_calificacion):
    with db_conector.get_db() as db:
        try:
            calificacion_obj = db.query(Calificaciones).filter(Calificaciones.ID_CALIFICACION == id_calificacion).first()
            if calificacion_obj:
                calificacion_obj.CALIFICACION = nueva_calificacion
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar calificación: {e}")
            return False

def obtener_todos_datos_calificaciones():
    with db_conector.get_db() as db:
        try:
            # Obtener todas las secciones
            secciones_data = db.query(
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION,
                Grados.NOMBRE_GRADO
            ).join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS).all()
            
            secciones = [s._asdict() for s in secciones_data]

            # Obtener todas las calificaciones
            calificaciones_data = db.query(
                Calificaciones.ID_CALIFICACION,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Materias.NOMBRE_MATERIA,
                Calificaciones.CALIFICACION,
                Calificaciones.FECHA_CALIFICACION,
                Secciones.NOMBRE_SECCION
            ).join(Estudiantes, Calificaciones.ID_EST == Estudiantes.ID_EST)\
            .join(Materias, Calificaciones.ID_MATERIA == Materias.ID_MATERIA)\
            .join(Secciones, Calificaciones.ID_SECCION == Secciones.ID_SECCION).all()
            
            calificaciones = [c._asdict() for c in calificaciones_data]

            return secciones, calificaciones
        except Exception as e:
            st.error(f"Error al obtener todos los datos de calificaciones: {e}")
            return None, None
