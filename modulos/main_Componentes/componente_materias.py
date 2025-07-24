from modulos.db_conector import get_db
from datetime import date # Usar date en lugar de datetime para fechas

# Importar modelos necesarios
from models import Materias, SeccionesMaterias, AsignacionEst, Calificaciones, Estudiantes, Secciones

# Función para agregar materia
def agregar_materia(nombre, descripcion):
    with get_db() as db:
        try:
            nueva_materia = Materias(
                NOMBRE_MATERIA=nombre,
                DESCRIPCION_MATERIA=descripcion,
                FECHA_CREACION=date.today()
            )
            db.add(nueva_materia)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al agregar la materia: {e}")
            return False

# Función para listar todas las materias
def listar_materias():
    with get_db() as db:
        try:
            resultados = db.query(Materias).all()
            materias = []
            for materia in resultados:
                materias.append({
                    "ID_MATERIA": materia.ID_MATERIA,
                    "NOMBRE_MATERIA": materia.NOMBRE_MATERIA,
                    "DESCRIPCION_MATERIA": materia.DESCRIPCION_MATERIA
                })
            return materias
        except Exception as e:
            print(f"Error al listar materias: {e}")
            return []

# Función para eliminar una materia por su ID
def eliminar_materia(id_materia):
    with get_db() as db:
        try:
            materia = db.query(Materias).filter(Materias.ID_MATERIA == id_materia).first()
            if materia:
                db.delete(materia)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar materia: {e}")
            return False

# Función para asignar una materia a una sección con fecha de registro
def asignar_materia_a_seccion(id_materia, id_seccion):
    try:
        with get_db() as db:
            # Insertar la materia en la sección
            nueva_seccion_materia = SeccionesMaterias(
                ID_MATERIA=id_materia,
                ID_SECCION=id_seccion,
                FECHA_CREACION=date.today()
            )
            db.add(nueva_seccion_materia)
            db.flush() # Para asegurar que la nueva_seccion_materia se persista antes de continuar

            # Obtener todos los estudiantes de la sección
            estudiantes = db.query(AsignacionEst.ID_EST).filter(
                AsignacionEst.ID_SECCION == id_seccion
            ).all()

            # Asignar la materia a todos los estudiantes de la sección con una calificación de 0
            for estudiante_id_tuple in estudiantes:
                estudiante_id = estudiante_id_tuple[0] # Extraer el ID de la tupla
                nueva_calificacion = Calificaciones(
                    ID_EST=estudiante_id,
                    ID_MATERIA=id_materia,
                    ID_SECCION=id_seccion,
                    CALIFICACION=0,
                    YEAR_ESCOLAR=date.today(), # Asumiendo que YEAR_ESCOLAR es un campo de fecha
                    FECHA_CALIFICACION=date.today()
                )
                db.add(nueva_calificacion)
            
            db.commit()
            return True
    except Exception as e:
        db.rollback()
        print(f"Error al asignar la materia a la sección: {e}")
        return False

def actualizar_materia(id_materia, nombre, descripcion):
    with get_db() as db:
        try:
            materia = db.query(Materias).filter(Materias.ID_MATERIA == id_materia).first()
            if materia:
                materia.NOMBRE_MATERIA = nombre
                materia.DESCRIPCION_MATERIA = descripcion
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar materia: {e}")
            return False
