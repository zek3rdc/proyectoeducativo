from modulos.db_conector import get_db
import streamlit as st
import datetime # Necesario para datetime.date.today()

# Importar modelos necesarios
from models import Grados, Secciones

def obtener_grados():
    """
    Obtiene la lista de grados desde la base de datos.
    """
    with get_db() as db:
        try:
            grados = db.query(Grados.ID_GRADOS, Grados.NOMBRE_GRADO).all()
            return grados
        except Exception as e:
            print(f"Error al obtener grados: {e}")
            return []

def agregar_grado(nombre_grado):
    """
    Agrega un nuevo grado a la base de datos.
    """
    with get_db() as db:
        try:
            nuevo_grado = Grados(
                NOMBRE_GRADO=nombre_grado,
                FECHA_CREACION=datetime.date.today()
            )
            db.add(nuevo_grado)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            st.error(f"Error al agregar el grado: {e}")
            return False

def modificar_grado(id_grado, nuevo_nombre):
    """
    Modifica el nombre de un grado existente.
    """
    with get_db() as db:
        try:
            grado = db.query(Grados).filter(Grados.ID_GRADOS == id_grado).first()
            if grado:
                grado.NOMBRE_GRADO = nuevo_nombre
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            st.error(f"Error al modificar el grado: {e}")
            return False

def eliminar_grado(id_grado):
    """
    Elimina un grado de la base de datos si no tiene secciones asociadas.
    """
    with get_db() as db:
        try:
            # Verificar si el grado tiene secciones asociadas
            secciones_asociadas = db.query(Secciones).filter(Secciones.ID_GRADO == id_grado).count()
            if secciones_asociadas > 0:
                st.warning("No se puede eliminar el grado porque tiene secciones asociadas.")
                return False
            
            # Eliminar el grado
            grado = db.query(Grados).filter(Grados.ID_GRADOS == id_grado).first()
            if grado:
                db.delete(grado)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            st.error(f"Error al eliminar el grado: {e}")
            return False

def asignar_grado_a_seccion(id_grado, id_seccion):
    """
    Asigna un grado a una sección existente.
    """
    with get_db() as db:
        try:
            seccion = db.query(Secciones).filter(Secciones.ID_SECCION == id_seccion).first()
            if seccion:
                seccion.ID_GRADO = id_grado
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            st.error(f"Error al asignar el grado a la sección: {e}")
            return False
