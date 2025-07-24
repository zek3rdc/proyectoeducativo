from modulos.db_conector import get_db
import datetime # Necesario para NOW()
from models import Profesores, Roles

def agregar_profesor(nombre, apellido, fecha_nac, cedula, email, telefono, direccion, codificacion, categoria, estudios, turno, estado, fecha_job, rol_nombre):
    """
    Agrega un nuevo profesor a la base de datos.
    """
    with get_db() as db:
        try:
            # Comprobar si el rol ya está registrado
            rol_existente = db.query(Roles).filter(Roles.ROL == rol_nombre).first()

            # Si el rol no existe, mostrar advertencia y salir
            if not rol_existente:
                raise ValueError("No hay un cargo designado. Por favor, dirígete al módulo de cargos para crear uno.")

            rol_id = rol_existente.ID_ROL

            # Crear instancia del nuevo profesor
            nuevo_profesor = Profesores(
                NOMBRE_PROF=nombre,
                APELLIDO_PROF=apellido,
                FECHA_NAC_PERSONAL=fecha_nac,
                CEDULA_PROF=cedula,
                EMAIL_PROF=email,
                TELEFONO_PROF=telefono,
                DIRECCION_PROF=direccion,
                CODIFICACION=codificacion,
                CATEGORIA=categoria,
                ESTUDIOS_ACTUAL=estudios,
                TURNO=turno,
                ESTADO=estado,
                FECHA_LABORAL=fecha_job,
                ID_ROL=rol_id,
                FECHA_REG_PROF=datetime.date.today() # Usar datetime.date.today()
            )
            db.add(nuevo_profesor)
            db.commit()
            return True
        except ValueError as ve:
            raise ve
        except Exception as e:
            db.rollback()
            print(f"Error al agregar el profesor: {e}")
            return False

def editar_profesor(id_profesor, nombre, apellido, fecha_nac, cedula, email, telefono, direccion, codificacion, categoria, estudios, turno, estado, fecha_job, rol_nombre):
    """
    Actualiza los datos de un profesor en la base de datos.
    """
    with get_db() as db:
        try:
            # Obtener el ID del rol a partir del nombre del rol
            rol_obj = db.query(Roles).filter(Roles.ROL == rol_nombre).first()
            if not rol_obj:
                raise ValueError(f"El rol '{rol_nombre}' no existe.")
            rol_id = rol_obj.ID_ROL

            profesor = db.query(Profesores).filter(Profesores.ID_PROF == id_profesor).first()
            if profesor:
                profesor.NOMBRE_PROF = nombre
                profesor.APELLIDO_PROF = apellido
                profesor.FECHA_NAC_PERSONAL = fecha_nac
                profesor.CEDULA_PROF = cedula
                profesor.EMAIL_PROF = email
                profesor.TELEFONO_PROF = telefono
                profesor.DIRECCION_PROF = direccion
                profesor.CODIFICACION = codificacion
                profesor.CATEGORIA = categoria
                profesor.ESTUDIOS_ACTUAL = estudios
                profesor.TURNO = turno
                profesor.ESTADO = estado
                profesor.FECHA_LABORAL = fecha_job
                profesor.ID_ROL = rol_id
                db.commit()
                return True
            return False
        except ValueError as ve:
            raise ve
        except Exception as e:
            db.rollback()
            print(f"Error al editar el profesor: {e}")
            return False

def eliminar_profesor(id_profesor):
    """
    Elimina un profesor de la base de datos.
    """
    with get_db() as db:
        try:
            profesor = db.query(Profesores).filter(Profesores.ID_PROF == id_profesor).first()
            if profesor:
                db.delete(profesor)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar profesor: {e}")
            return False

def listar_roles():
    """
    Obtiene la lista de roles desde la base de datos.
    """
    with get_db() as db:
        try:
            roles = db.query(Roles.ROL).all()
            return [r.ROL for r in roles]
        except Exception as e:
            print(f"Error al listar roles: {e}")
            return []

def agregar_rol(rol_nombre):
    """
    Inserta un nuevo rol en la base de datos en la tabla "ROLES".
    """
    with get_db() as db:
        try:
            nuevo_rol = Roles(ROL=rol_nombre)
            db.add(nuevo_rol)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al agregar el rol: {e}")
            return False

def editar_rol(rol_actual, nuevo_rol):
    """
    Actualiza el nombre de un rol en la tabla "ROLES".
    """
    with get_db() as db:
        try:
            rol_obj = db.query(Roles).filter(Roles.ROL == rol_actual).first()
            if rol_obj:
                rol_obj.ROL = nuevo_rol
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al ejecutar la consulta: {e}")
            raise

def eliminar_rol(rol_nombre):
    """
    Elimina un rol de la base de datos en la tabla "ROLES".
    """
    with get_db() as db:
        try:
            rol_obj = db.query(Roles).filter(Roles.ROL == rol_nombre).first()
            if rol_obj:
                db.delete(rol_obj)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar rol: {e}")
            return False
