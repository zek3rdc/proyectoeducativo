from modulos.db_conector import get_db
import datetime # Necesario para NOW()
from models import Representantes, TelefonosRepre

def obtener_representantes():
    with get_db() as db:
        try:
            representantes = db.query(Representantes).all()
            return [r.__dict__ for r in representantes] # Convertir a diccionario para compatibilidad
        except Exception as e:
            print(f"Error al obtener representantes: {e}")
            return []

def agregar_representante(nombre, apellido, cedula, telefono_principal, direccion, fecha_nac, telefonos_adicionales=""):
    try:
        with get_db() as db:
            # Primero insertar el representante
            nuevo_representante = Representantes(
                NOMBRE_REP=nombre,
                APELLIDO_REP=apellido,
                CEDULA_REP=cedula,
                DIRECCION_REP=direccion,
                TELEFONO_REP=telefono_principal,
                FECHA_NAC_REP=fecha_nac,
                FECHA_REG_REP=datetime.date.today()
            )
            db.add(nuevo_representante)
            db.flush() # Para obtener el ID_REP generado

            id_rep = nuevo_representante.ID_REP
            
            # Ahora agregar el teléfono principal
            agregar_telefono(id_rep, telefono_principal, db)

            # Agregar teléfonos adicionales, si existen
            if telefonos_adicionales:
                for telefono in telefonos_adicionales.split(","):
                    telefono = telefono.strip()
                    if telefono:
                        agregar_telefono(id_rep, telefono, db)
            
            db.commit() # Confirmar todas las operaciones
            return {"ID_REP": id_rep}
    
    except ValueError as ve:
        db.rollback()
        return {"error": str(ve)}
    except Exception as e:
        db.rollback()
        return {"error": f"Error inesperado: {str(e)}"}


def agregar_telefono(id_rep, telefono, db_session):
    # Verificar si el ID_REP existe en la tabla REPRESENTANTES
    representante_existe = db_session.query(Representantes).filter(Representantes.ID_REP == id_rep).first()
    
    if representante_existe:
        nuevo_telefono = TelefonosRepre(
            ID_REP=id_rep,
            TELEFONO=telefono,
            FECHA_REG=datetime.date.today()
        )
        db_session.add(nuevo_telefono)
        # No hacemos commit aquí, se hará en la función principal (agregar_representante)
    else:
        raise ValueError(f"El ID_REP {id_rep} no existe en la tabla REPRESENTANTES.")


def eliminar_representante(id_rep):
    with get_db() as db:
        try:
            # Eliminar teléfonos asociados primero
            db.query(TelefonosRepre).filter(TelefonosRepre.ID_REP == id_rep).delete()
            
            # Luego eliminar el representante
            representante = db.query(Representantes).filter(Representantes.ID_REP == id_rep).first()
            if representante:
                db.delete(representante)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar representante: {e}")
            return False

def actualizar_representante(id_rep, nombre, apellido, cedula, telefono, direccion):
    with get_db() as db:
        try:
            representante = db.query(Representantes).filter(Representantes.ID_REP == id_rep).first()
            if representante:
                representante.NOMBRE_REP = nombre
                representante.APELLIDO_REP = apellido
                representante.CEDULA_REP = cedula
                representante.TELEFONO_REP = telefono
                representante.DIRECCION_REP = direccion
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al actualizar representante: {e}")
            return False

def obtener_telefonos_representante(id_rep):
    with get_db() as db:
        try:
            telefonos = db.query(TelefonosRepre.TELEFONO).filter(TelefonosRepre.ID_REP == id_rep).all()
            return [t.TELEFONO for t in telefonos]
        except Exception as e:
            print(f"Error al obtener los teléfonos: {e}")
            return []

def eliminar_telefonos_representante(id_rep):
    with get_db() as db:
        try:
            db.query(TelefonosRepre).filter(TelefonosRepre.ID_REP == id_rep).delete()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error al eliminar teléfonos del representante: {e}")
            return False
