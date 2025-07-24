from datetime import date
from modulos.db_conector import get_db # Importar get_db directamente
import streamlit as st

# Importar modelos necesarios
from models import Secciones, Grados, Profesores, Roles

def agregar_seccion_db(nombre_seccion, grado_id, profesor_id):
    """
    Inserta una nueva sección en la base de datos.
    """
    with get_db() as db:
        try:
            nueva_seccion = Secciones(
                NOMBRE_SECCION=nombre_seccion,
                ID_GRADO=grado_id,
                ID_PROF=profesor_id,
                FECHA_CREA_ASIG=date.today()
            )
            db.add(nueva_seccion)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al agregar la sección: {e}")
            return False

def obtener_profesores():
    """
    Obtiene los profesores con el rol 'PROFESOR' desde la base de datos.
    """
    with get_db() as db:
        try:
            profesores_data = db.query(
                Profesores.ID_PROF.label('id_profesor'),
                Profesores.NOMBRE_PROF.label('nombre'),
                Profesores.APELLIDO_PROF.label('apellido'),
                Profesores.CEDULA_PROF.label('cedula'),
                Roles.ROL.label('rol')
            ).join(Roles, Profesores.ID_ROL == Roles.ID_ROL)\
            .order_by(Profesores.NOMBRE_PROF.asc()).all()
            
            return [p._asdict() for p in profesores_data]
        except Exception as e:
            st.error(f"Error al obtener los profesores: {e}")
            return []

def editar_seccion_db(id_seccion, nuevo_nombre, id_grado, id_profesor):
    with get_db() as db:
        try:
            seccion = db.query(Secciones).filter(Secciones.ID_SECCION == id_seccion).first()
            if seccion:
                seccion.NOMBRE_SECCION = nuevo_nombre
                seccion.ID_GRADO = id_grado
                seccion.ID_PROF = id_profesor
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al editar la sección: {e}")
            return False

def obtener_grados():
    with get_db() as db:
        try:
            grados = db.query(Grados.ID_GRADOS, Grados.NOMBRE_GRADO).order_by(Grados.NOMBRE_GRADO.asc()).all()
            return grados
        except Exception as e:
            st.error(f"Error al obtener los grados: {e}")
            return []

def rename_fields(materias):
    """
    Renombra las columnas de las materias y devuelve la lista de diccionarios con las columnas renombradas.
    """
    if not materias:
        raise ValueError("No se encontraron materias para el grado especificado.")
    
    mapeo_columnas = {
        'id_seccion': 'ID Sección',
        'nombre_seccion': 'Nombre Sección',
        'id_grado': 'ID Grado',
        'nombre_grado': 'Nombre Grado',
        'id_profesor': 'ID Profesor',
        'nombre_profesor': 'Nombre Profesor',
        'cedula_profesor': 'Cédula Profesor',
        'id_materia': 'ID Materia',
        'nombre_materia': 'Nombre Materia',
        'descripcion_materia': 'Descripción Materia'
    }

    materias_renombradas = [
        {mapeo_columnas.get(key, key): value for key, value in materia.items()}
        for materia in materias
    ]
    
    return materias_renombradas

def obtener_personal_por_rol(rol_seleccionado):
    """
    Obtiene una lista de personal asociado a un rol específico.
    """
    with get_db() as db:
        try:
            personal_data = db.query(
                Profesores.ID_PROF,
                Profesores.NOMBRE_PROF,
                Profesores.APELLIDO_PROF,
                Profesores.CEDULA_PROF
            ).join(Roles, Profesores.ID_ROL == Roles.ID_ROL)\
            .filter(Roles.ROL == rol_seleccionado)\
            .order_by(Profesores.NOMBRE_PROF.asc()).all()
            
            return personal_data # Retorna lista de tuplas
        except Exception as e:
            print(f"Error al obtener personal por rol: {e}")
            return []

def obtener_roles():
    """
    Obtiene una lista de todos los roles disponibles en la base de datos.
    """
    with get_db() as db:
        try:
            roles = db.query(Roles.ID_ROL, Roles.ROL).order_by(Roles.ROL.asc()).all()
            return roles
        except Exception as e:
            print(f"Error al obtener roles: {e}")
            return []
