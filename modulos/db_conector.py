from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    AsignacionEst, AsistenciaEstudiantes, AsistenciaProfesores, Calificaciones,
    Estudiantes, Grados, Incidencias, Materias, Profesores, Representantes,
    RepreEst, Roles, Secciones, SeccionesMaterias, TelefonosRepre
)
import pandas as pd
from contextlib import contextmanager
from sqlalchemy import func

# Context manager para obtener una sesión de base de datos
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para ejecutar una modificación (INSERT, UPDATE, DELETE)
def ejecutar_modificacion(model_instance=None, query=None, params=None):
    with get_db() as db:
        try:
            if model_instance:
                db.add(model_instance)
                db.commit()
                db.refresh(model_instance)
                return model_instance
            elif query:
                # Para consultas SQL directas que modifican datos
                result = db.execute(query, params)
                db.commit()
                return result.rowcount
            return None
        except Exception as e:
            db.rollback()
            print(f"Error al ejecutar la modificación: {e}")
            return None

# Función para ejecutar una consulta SELECT
def ejecutar_consulta(query=None, params=None, fetch_all=True, model=None):
    with get_db() as db:
        try:
            if model:
                if fetch_all:
                    return db.query(model).filter_by(**params).all() if params else db.query(model).all()
                else:
                    return db.query(model).filter_by(**params).first() if params else db.query(model).first()
            elif query:
                # Para consultas SQL directas que recuperan datos
                result = db.execute(query, params)
                if fetch_all:
                    return result.fetchall()
                else:
                    return result.fetchone()
            return None
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

# Consultar ESTUDIANTES
def obtener_ESTUDIANTES_1():
    with get_db() as db:
        try:
            # Usando el ORM para construir la consulta
            estudiantes_data = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Estudiantes.CEDULA.label("CI_EST"),
                Estudiantes.CEDULA_EST,
                Estudiantes.EMAIL_EST,
                Estudiantes.TELEFONO_EST,
                Estudiantes.ESTADO,
                Estudiantes.DESCRIPCION_ESTADO.label("DESCRIPCION"),
                Estudiantes.GENERO,
                Estudiantes.CONDICION,
                Representantes.ID_REP,
                Representantes.NOMBRE_REP.label("NOMBRE_REPRE"),
                Representantes.APELLIDO_REP.label("APELLIDO_REPRE"),
                Representantes.CEDULA_REP,
                Estudiantes.FECHA_REG,
                Secciones.NOMBRE_SECCION.label("SECCION_ASIGNADA")
            ).join(RepreEst, Estudiantes.ID_EST == RepreEst.ID_EST)\
            .join(Representantes, Representantes.ID_REP == RepreEst.ID_REPRE)\
            .outerjoin(AsignacionEst, Estudiantes.ID_EST == AsignacionEst.ID_EST)\
            .outerjoin(Secciones, AsignacionEst.ID_SECCION == Secciones.ID_SECCION)\
            .filter(RepreEst.ESTADO == 'ACTIVO').all()

            # Convertir los resultados a una lista de diccionarios para mantener la compatibilidad
            return [row._asdict() for row in estudiantes_data]
        except Exception as e:
            print(f"Error al consultar ESTUDIANTES: {e}")
            return None

def obtener_padres():
    with get_db() as db:
        try:
            representantes = db.query(Representantes).order_by(Representantes.ID_REP.asc()).all()
            return [r.__dict__ for r in representantes] # Convertir a diccionario si es necesario
        except Exception as e:
            print(f"Error al consultar Representantes: {e}")
            return None

def obtener_ultimo_ID_EST():
    with get_db() as db:
        try:
            ultimo_id = db.query(func.max(Estudiantes.ID_EST)).scalar()
            return ultimo_id
        except Exception as e:
            print(f"Error al obtener el último ID de estudiante: {e}")
            return None


def registro_existe(model, field, value):
    with get_db() as db:
        try:
            count = db.query(model).filter(field == value).count()
            return count > 0
        except Exception as e:
            print(f"Error al consultar registro en {model.__tablename__}.{field.name}={value}: {e}")
            return False

def matricula_existe(cedula_EST):
    return registro_existe(Estudiantes, Estudiantes.CEDULA_EST, cedula_EST)

def cedula_existe(cedula):
    return registro_existe(Estudiantes, Estudiantes.CEDULA, cedula)

def cambiar_estado_estudiante(ID_EST, nuevo_estado, descripcion):
    with get_db() as db:
        try:
            estudiante = db.query(Estudiantes).filter(Estudiantes.ID_EST == ID_EST).first()
            if estudiante:
                estudiante.ESTADO = nuevo_estado
                estudiante.DESCRIPCION_ESTADO = descripcion # Asumiendo que DESCRIPCION_ESTADO es la columna correcta
                db.commit()
                print(f"Estado del estudiante con ID {ID_EST} actualizado.")
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al cambiar el estado del estudiante: {e}")
            return False

# Las funciones ejecutar_consulta_unica y obtener_datos se pueden reemplazar por ejecutar_consulta
# o por consultas directas al ORM.

def obtener_secciones():
    with get_db() as db:
        try:
            secciones_data = db.query(
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION,
                Grados.NOMBRE_GRADO,
                (Profesores.NOMBRE_PROF + ' ' + Profesores.APELLIDO_PROF).label("PROFESOR")
            ).join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .order_by(Secciones.ID_SECCION.asc()).all()
            
            return [row._asdict() for row in secciones_data]
        except Exception as e:
            print(f"Error al obtener secciones: {e}")
            return []

def obtener_materias_por_grado(grado_nombre):
    with get_db() as db:
        try:
            # Asumiendo que existe una tabla GRADO_MATERIAS o una relación directa
            # Si no existe, esta función necesitará una revisión más profunda.
            # Por ahora, asumo una relación a través de SeccionesMaterias y Grados
            materias = db.query(Materias.NOMBRE_MATERIA)\
                       .join(SeccionesMaterias, Materias.ID_MATERIA == SeccionesMaterias.ID_MATERIA)\
                       .join(Secciones, SeccionesMaterias.ID_SECCION == Secciones.ID_SECCION)\
                       .join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
                       .filter(Grados.NOMBRE_GRADO == grado_nombre).distinct().all()
            return [m[0] for m in materias]
        except Exception as e:
            print(f"Error al obtener materias por grado: {e}")
            return []

def obtener_asistencia_estudiantes(id_seccion):
    with get_db() as db:
        try:
            asistencia_data = db.query(
                (Estudiantes.NOMBRE_EST + ' ' + Estudiantes.APELLIDO_EST).label("ESTUDIANTE"),
                AsistenciaEstudiantes.FECHA_ASISTENCIA,
                AsistenciaEstudiantes.ESTADO_ASISTENCIA
            ).join(Estudiantes, AsistenciaEstudiantes.ID_EST == Estudiantes.ID_EST)\
            .filter(AsistenciaEstudiantes.ID_SECCION == id_seccion).all()
            
            return [row._asdict() for row in asistencia_data]
        except Exception as e:
            print(f"Error al obtener asistencia de estudiantes: {e}")
            return []

def obtener_asistencia_profesores(id_seccion):
    with get_db() as db:
        try:
            # La tabla ASISTENCIA_PROFESORES no tiene ID_SECCION.
            # Si la intención es obtener la asistencia del profesor asignado a esa sección,
            # se necesita una unión a la tabla SECCIONES.
            # Asumo que se quiere la asistencia de los profesores que imparten clases en esa sección.
            asistencia_data = db.query(
                (Profesores.NOMBRE_PROF + ' ' + Profesores.APELLIDO_PROF).label("PROFESOR"),
                AsistenciaProfesores.FECHA_ASISTENCIA,
                AsistenciaProfesores.ESTADO_ASISTENCIA
            ).join(Profesores, AsistenciaProfesores.ID_PROF == Profesores.ID_PROF)\
            .join(Secciones, Profesores.ID_PROF == Secciones.ID_PROF)\
            .filter(Secciones.ID_SECCION == id_seccion).all()
            
            return [row._asdict() for row in asistencia_data]
        except Exception as e:
            print(f"Error al obtener asistencia de profesores: {e}")
            return []

def obtener_calificaciones_estudiantes(id_seccion):
    with get_db() as db:
        try:
            calificaciones_data = db.query(
                (Estudiantes.NOMBRE_EST + ' ' + Estudiantes.APELLIDO_EST).label("ESTUDIANTE"),
                Materias.NOMBRE_MATERIA,
                Calificaciones.CALIFICACION
            ).join(Estudiantes, Calificaciones.ID_EST == Estudiantes.ID_EST)\
            .join(Materias, Calificaciones.ID_MATERIA == Materias.ID_MATERIA)\
            .filter(Calificaciones.ID_SECCION == id_seccion).all()
            
            return [row._asdict() for row in calificaciones_data]
        except Exception as e:
            print(f"Error al obtener calificaciones de estudiantes: {e}")
            return []

def listar_secciones():
    with get_db() as db:
        try:
            secciones = db.query(
                Secciones.ID_SECCION.label("id_seccion"),
                Secciones.NOMBRE_SECCION.label("nombre_seccion"),
                Secciones.ID_GRADO.label("grado"),
                Secciones.ID_PROF.label("profesor")
            ).all()
            return [s._asdict() for s in secciones]
        except Exception as e:
            print(f"Error al listar secciones: {e}")
            return []

def listar_detalles_seccion(id_seccion):
    if not isinstance(id_seccion, int):
        raise ValueError(f"El ID de la sección debe ser un número entero. Se recibió: {id_seccion}")

    with get_db() as db:
        try:
            detalles = db.query(
                Secciones.ID_SECCION.label("id_seccion"),
                Secciones.NOMBRE_SECCION.label("nombre_seccion"),
                Secciones.ID_GRADO.label("id_grado"),
                Grados.NOMBRE_GRADO.label("nombre_grado"),
                Profesores.NOMBRE_PROF.label("nombre_profesor"),
                Profesores.CEDULA_PROF.label("cedula_profesor"),
                Materias.ID_MATERIA.label("id_materia"),
                Materias.NOMBRE_MATERIA.label("nombre_materia"),
                Materias.DESCRIPCION_MATERIA.label("descripcion_materia")
            ).join(SeccionesMaterias, Secciones.ID_SECCION == SeccionesMaterias.ID_SECCION)\
            .join(Materias, SeccionesMaterias.ID_MATERIA == Materias.ID_MATERIA)\
            .join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .filter(Secciones.ID_SECCION == id_seccion).all()
            
            return [d._asdict() for d in detalles]
        except Exception as e:
            print(f"Error al listar detalles de sección: {e}")
            return []

def listar_asistencia_estudiantes(id_seccion):
    with get_db() as db:
        try:
            asistencia = db.query(
                AsistenciaEstudiantes.ID_EST.label("id_estudiante"),
                Estudiantes.NOMBRE_EST.label("nombre"),
                AsistenciaEstudiantes.FECHA_ASISTENCIA.label("fecha"),
                AsistenciaEstudiantes.ESTADO_ASISTENCIA.label("estado")
            ).join(Estudiantes, AsistenciaEstudiantes.ID_EST == Estudiantes.ID_EST)\
            .filter(AsistenciaEstudiantes.ID_SECCION == id_seccion).all()
            
            return [a._asdict() for a in asistencia]
        except Exception as e:
            print(f"Error al listar asistencia de estudiantes: {e}")
            return []

def listar_asistencia_profesores(id_seccion):
    with get_db() as db:
        try:
            # Similar a obtener_asistencia_profesores, asumo que se refiere al profesor de la sección
            asistencia = db.query(
                Profesores.ID_PROF.label("id_profesor"),
                Profesores.NOMBRE_PROF.label("nombre"),
                AsistenciaProfesores.FECHA_ASISTENCIA.label("fecha"),
                AsistenciaProfesores.ESTADO_ASISTENCIA.label("estado")
            ).join(Profesores, AsistenciaProfesores.ID_PROF == Profesores.ID_PROF)\
            .join(Secciones, Profesores.ID_PROF == Secciones.ID_PROF)\
            .filter(Secciones.ID_SECCION == id_seccion).all()
            
            return [a._asdict() for a in asistencia]
        except Exception as e:
            print(f"Error al listar asistencia de profesores: {e}")
            return []

def listar_calificaciones(id_seccion):
    with get_db() as db:
        try:
            calificaciones = db.query(
                Calificaciones.ID_EST.label("id_estudiante"),
                Estudiantes.NOMBRE_EST.label("nombre"),
                Materias.NOMBRE_MATERIA.label("materia"),
                Calificaciones.CALIFICACION.label("calificacion"),
                Calificaciones.FECHA_CALIFICACION.label("fecha")
            ).join(Estudiantes, Calificaciones.ID_EST == Estudiantes.ID_EST)\
            .join(Materias, Calificaciones.ID_MATERIA == Materias.ID_MATERIA)\
            .filter(Calificaciones.ID_SECCION == id_seccion).all()
            
            return [c._asdict() for c in calificaciones]
        except Exception as e:
            print(f"Error al listar calificaciones: {e}")
            return []

def listar_profesores():
    with get_db() as db:
        try:
            profesores_data = db.query(
                Profesores.ID_PROF.label("id_profesor"),
                Profesores.NOMBRE_PROF.label("nombre"),
                Profesores.APELLIDO_PROF.label("apellido"),
                Profesores.CEDULA_PROF.label("cedula"),
                Profesores.TELEFONO_PROF.label("telefono"),
                Profesores.DIRECCION_PROF.label("direccion"),
                Profesores.FECHA_NAC_PERSONAL.label("fecha_nacimiento"),
                Profesores.CODIFICACION.label("codificacion"),
                Profesores.CATEGORIA.label("categoria"),
                Profesores.ESTUDIOS_ACTUAL.label("estudios_actual"),
                Profesores.FECHA_LABORAL.label("fecha_laboral"),
                Profesores.EMAIL_PROF.label("email"),
                Profesores.TURNO.label("Turno"),
                Profesores.ESTADO.label("estado"),
                func.coalesce(Roles.ROL, 'Sin Rol').label("rol")
            ).outerjoin(Roles, Profesores.ID_ROL == Roles.ID_ROL).all()
            
            return [p._asdict() for p in profesores_data]
        except Exception as e:
            print(f"Error al listar profesores: {e}")
            return []

def obtener_secciones_rendimiento():
    with get_db() as db:
        try:
            secciones = db.query(Secciones.ID_SECCION, Secciones.NOMBRE_SECCION).distinct().all()
            return [f"{row.ID_SECCION} - {row.NOMBRE_SECCION}" for row in secciones]
        except Exception as e:
            print(f"Error al obtener secciones para rendimiento: {e}")
            return []

def obtener_materias():
    with get_db() as db:
        try:
            materias = db.query(Materias.ID_MATERIA, Materias.NOMBRE_MATERIA).distinct().all()
            return [f"{row.ID_MATERIA} - {row.NOMBRE_MATERIA}" for row in materias]
        except Exception as e:
            print(f"Error al obtener materias: {e}")
            return []

def obtener_anios_escolares():
    with get_db() as db:
        try:
            anios = db.query(Calificaciones.YEAR_ESCOLAR).distinct().order_by(Calificaciones.YEAR_ESCOLAR.desc()).all()
            return [a[0] for a in anios]
        except Exception as e:
            print(f"Error al obtener años escolares: {e}")
            return []

def obtener_calificaciones(seccion, materia, year_escolar):
    with get_db() as db:
        try:
            query = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Calificaciones.CALIFICACION,
                Materias.NOMBRE_MATERIA,
                Secciones.NOMBRE_SECCION,
                Calificaciones.YEAR_ESCOLAR,
                Calificaciones.FECHA_CALIFICACION
            ).join(Estudiantes, Calificaciones.ID_EST == Estudiantes.ID_EST)\
            .join(Materias, Calificaciones.ID_MATERIA == Materias.ID_MATERIA)\
            .join(Secciones, Calificaciones.ID_SECCION == Secciones.ID_SECCION)

            if seccion != "Ver Todo":
                id_seccion = int(seccion.split(" - ")[0])
                query = query.filter(Calificaciones.ID_SECCION == id_seccion)
            if materia != "Ver Todo":
                id_materia = int(materia.split(" - ")[0])
                query = query.filter(Calificaciones.ID_MATERIA == id_materia)
            if year_escolar != "Ver Todo":
                query = query.filter(Calificaciones.YEAR_ESCOLAR == year_escolar)

            resultados = query.order_by(Calificaciones.FECHA_CALIFICACION.desc()).all()
            return pd.DataFrame([r._asdict() for r in resultados])
        except Exception as e:
            print(f"Error al obtener calificaciones: {e}")
            return pd.DataFrame()

def asignar_estudiante_a_seccion(id_estudiante, id_seccion):
    from datetime import date
    with get_db() as db:
        try:
            id_estudiante = int(id_estudiante)
            id_seccion = int(id_seccion)

            # Verificar si el estudiante ya está asignado a la sección
            existing_assignment = db.query(AsignacionEst).filter(
                AsignacionEst.ID_EST == id_estudiante,
                AsignacionEst.ID_SECCION == id_seccion
            ).first()

            if existing_assignment:
                print(f"El estudiante {id_estudiante} ya está asignado a la sección {id_seccion}.")
                return False

            # Insertar la asignación del estudiante a la sección
            new_assignment = AsignacionEst(
                ID_EST=id_estudiante,
                ID_SECCION=id_seccion,
                YEAR_ESCOLAR=date.today(),
                FECHA_ASIGNACION=date.today()
            )
            db.add(new_assignment)
            db.flush() # Para que el objeto tenga ID_ASIGNACION si es necesario

            # Obtener las materias asociadas a la sección
            materias_seccion = db.query(SeccionesMaterias.ID_MATERIA).filter(
                SeccionesMaterias.ID_SECCION == id_seccion
            ).all()

            if not materias_seccion:
                print("La sección no tiene materias asignadas.")
                db.rollback()
                return False

            # Asignar las materias al estudiante con una calificación de 0
            for materia_id_tuple in materias_seccion:
                materia_id = materia_id_tuple[0] # Extraer el ID de la tupla
                new_calificacion = Calificaciones(
                    ID_EST=id_estudiante,
                    ID_MATERIA=materia_id,
                    ID_SECCION=id_seccion,
                    CALIFICACION=0,
                    YEAR_ESCOLAR=date.today(),
                    FECHA_CALIFICACION=date.today()
                )
                db.add(new_calificacion)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al asignar el estudiante a la sección: {e}")
            return False

def obtener_estudiantes_por_seccion(id_seccion):
    with get_db() as db:
        try:
            id_seccion = int(id_seccion)
            estudiantes = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Estudiantes.CEDULA,
                Estudiantes.CEDULA_EST
            ).join(AsignacionEst, Estudiantes.ID_EST == AsignacionEst.ID_EST)\
            .filter(AsignacionEst.ID_SECCION == id_seccion)\
            .order_by(Estudiantes.NOMBRE_EST.asc()).all()
            
            return [e._asdict() for e in estudiantes]
        except Exception as e:
            print(f"Error al obtener estudiantes por sección: {e}")
            return []

def insertar_id_acceso_en_base_de_datos(id_profesor, id_acceso):
    with get_db() as db:
        try:
            profesor = db.query(Profesores).filter(Profesores.ID_PROF == id_profesor).first()
            if profesor:
                profesor.ID_ACCESO = id_acceso
                db.commit()
                return "ID de acceso actualizado exitosamente en la base de datos."
            return "Profesor no encontrado."
        except Exception as e:
            db.rollback()
            return f"Error al actualizar ID de acceso en la base de datos: {e}"

def obtener_estudiantes_con_seccion():
    with get_db() as db:
        try:
            estudiantes_seccion = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                AsignacionEst.ID_SECCION,
                Secciones.NOMBRE_SECCION
            ).join(AsignacionEst, Estudiantes.ID_EST == AsignacionEst.ID_EST)\
            .join(Secciones, AsignacionEst.ID_SECCION == Secciones.ID_SECCION).all()
            
            return [e._asdict() for e in estudiantes_seccion]
        except Exception as e:
            print(f"Error al obtener los estudiantes con sección: {e}")
            return None

def eliminar_estudiante_de_seccion(id_estudiante):
    with get_db() as db:
        try:
            # Eliminar las calificaciones del estudiante
            db.query(Calificaciones).filter(Calificaciones.ID_EST == id_estudiante).delete()
            
            # Eliminar la asignación del estudiante de la sección
            db.query(AsignacionEst).filter(AsignacionEst.ID_EST == id_estudiante).delete()
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar al estudiante de la sección: {e}")
            return False
