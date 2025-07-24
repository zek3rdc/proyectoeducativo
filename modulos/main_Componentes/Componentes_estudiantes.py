from modulos import db_conector
import pandas as pd
import datetime
import os
from PIL import Image
import streamlit as st
# Eliminar: import psycopg2
# Eliminar: from psycopg2 import OperationalError
# Eliminar: from psycopg2.extras import RealDictCursor

# Importar modelos necesarios
from models import Estudiantes, RepreEst, AsignacionEst, Secciones, Representantes, Calificaciones, Materias, Grados, Profesores, AsistenciaEstudiantes, AsistenciaProfesores

def renombrar_columnas(df):
    return df.rename(columns={
        'ID_EST': 'ID Estudiante',
        'NOMBRE_EST': 'Nombre Estudiante',
        'APELLIDO_EST': 'Apellido Estudiante',
        'CI_EST': 'Cédula Identidad',
        'CEDULA_EST': 'Cédula Estudiantil',
        "TELEFONO_EST": "Telefono Estudiante",
        "EMAIL_EST": "Email Estudiante",
        'ESTADO': 'Estado',
        'DESCRIPCION': 'Descripción Estado',
        'GENERO': 'Género',
        'CONDICION': 'Condición',
        'ID_REP': 'ID Representante',
        'NOMBRE_REPRE': 'Nombre Representante',
        'APELLIDO_REPRE': 'Apellido Representante',
        'CEDULA_REP': 'Cédula Representante',
        'FECHA_REG': 'Fecha de Registro',
        'SECCION_ASIGNADA': 'Sección Asignada'
    })

# Agregar un estudiante
def agregar_estudiante(nombre, apellido, cedula, cedula_est, id_representante, genero, estado, condicion, fecha_nac, email, telefono):
    try:
        # Validar si la cédula ya existe (solo si no es NULL)
        if cedula and db_conector.cedula_existe(cedula):
            return f"⚠️ La cédula {cedula} ya está registrada en la base de datos."

        # Validar si la matrícula ya existe (solo si no es NULL)
        if cedula_est and db_conector.matricula_existe(cedula_est):
            return f"⚠️ La matrícula {cedula_est} ya está registrada en la base de datos."

        # Crear instancia del estudiante
        nuevo_estudiante = Estudiantes(
            NOMBRE_EST=nombre,
            APELLIDO_EST=apellido,
            CEDULA=cedula,
            CEDULA_EST=cedula_est,
            GENERO=genero,
            ESTADO=estado,
            CONDICION=condicion,
            FECHA_NAC=fecha_nac,
            FECHA_REG=datetime.date.today(), # Usar datetime.date.today()
            EMAIL_EST=email,
            TELEFONO_EST=telefono,
            DESCRIPCION_ESTADO='RECIÉN AGREGADO'
        )
        
        # Insertar el estudiante usando la nueva función de db_conector
        estudiante_agregado = db_conector.ejecutar_modificacion(model_instance=nuevo_estudiante)
        
        if not estudiante_agregado:
            raise ValueError("No se pudo agregar el estudiante.")
        
        id_nuevo_estudiante = estudiante_agregado.ID_EST

        # Enlazar el estudiante con el representante
        if id_representante:
            nueva_relacion_repre_est = RepreEst(
                ID_REPRE=id_representante,
                ID_EST=id_nuevo_estudiante,
                ESTADO='ACTIVO',
                FECHA_REG=datetime.date.today() # Usar datetime.date.today()
            )
            db_conector.ejecutar_modificacion(model_instance=nueva_relacion_repre_est)

        return id_nuevo_estudiante

    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def modificar_estudiante(id_estudiante, nuevo_nombre, nuevo_apellido, nueva_cedula, nueva_cedula_est, 
                         nuevo_genero, nueva_condicion, nuevo_email, nuevo_telefono):
    """
    Modifica los datos generales de un estudiante en la base de datos.
    """
    try:
        genero_normalizado = nuevo_genero.lower()
        if genero_normalizado not in ["varon", "hembra"]:
            raise ValueError("El género proporcionado no es válido. Debe ser 'varon' o 'hembra'.")

        if not nueva_condicion or nueva_condicion.strip() == "":
            nueva_condicion = "no"

        with db_conector.get_db() as db:
            estudiante = db.query(Estudiantes).filter(Estudiantes.ID_EST == id_estudiante).first()
            if estudiante:
                estudiante.NOMBRE_EST = nuevo_nombre
                estudiante.APELLIDO_EST = nuevo_apellido
                estudiante.CEDULA = nueva_cedula
                estudiante.CEDULA_EST = nueva_cedula_est
                estudiante.GENERO = genero_normalizado
                estudiante.CONDICION = nueva_condicion
                estudiante.EMAIL_EST = nuevo_email
                estudiante.TELEFONO_EST = nuevo_telefono
                db.commit()
                return True
            return False
    except Exception as e:
        print(f"Error al modificar el estudiante: {e}")
        return False

def modificar_representante(id_estudiante, nuevo_id_representante, razon_cambio):
    """
    Modifica el representante de un estudiante y agrega un log del cambio realizado.
    """
    try:
        with db_conector.get_db() as db:
            # Recuperar la relación actual del estudiante (solo si el estado es "ACTIVO")
            relacion_actual = db.query(RepreEst).filter(
                RepreEst.ID_EST == id_estudiante,
                RepreEst.ESTADO == 'ACTIVO'
            ).first()

            id_representante_actual = None
            if relacion_actual:
                id_representante_actual = relacion_actual.ID_REPRE
                # Si el representante es diferente, cambiar el estado de la relación anterior a "ALTERADO"
                if id_representante_actual != nuevo_id_representante:
                    relacion_actual.ESTADO = 'ALTERADO'
                    db.add(relacion_actual) # Marcar para actualización
                    db.flush() # Asegurar que el cambio se refleje antes de la nueva inserción

            # Insertar la nueva relación con el nuevo representante y marcarla como "ACTIVO"
            mensaje_cambio = f"Representante anterior (ID {id_representante_actual}) cambiado por nuevo representante (ID {nuevo_id_representante})"
            nueva_relacion = RepreEst(
                ID_REPRE=nuevo_id_representante,
                ID_EST=id_estudiante,
                RAZON=razon_cambio,
                FECHA_CAMBIO=datetime.date.today(),
                CAMBIO_DE=mensaje_cambio,
                ESTADO='ACTIVO',
                FECHA_REG=datetime.date.today() # Asumiendo que FECHA_REG también se actualiza o se establece
            )
            db.add(nueva_relacion)
            db.commit()
            return True
    except Exception as e:
        db.rollback()
        print(f"Error al modificar el representante: {e}")
        return False

# Eliminar un estudiante
def eliminar_estudiante(id_est):
    try:
        # La función db_conector.eliminar_estudiante_de_seccion ya maneja CALIFICACIONES y ASIGNACION_EST
        db_conector.eliminar_estudiante_de_seccion(id_est)

        with db_conector.get_db() as db:
            # Eliminar relaciones en "REPRE_EST"
            db.query(RepreEst).filter(RepreEst.ID_EST == id_est).delete()
            
            # Eliminar el estudiante de la tabla "ESTUDIANTES"
            db.query(Estudiantes).filter(Estudiantes.ID_EST == id_est).delete()
            db.commit()
            return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar estudiante: {e}")
        return False

# Cambiar estado del estudiante (esta función ya llama a db_conector.cambiar_estado_estudiante, que ya fue refactorizada)
# No necesita cambios aquí, solo se asegura que la llamada sea correcta.
# def cambiar_estado_estudiante(id_est, nuevo_estado, descripcion):
#     db_conector.cambiar_estado_estudiante(id_est, nuevo_estado, descripcion)

def guardar_imagen_estudiante(id_estudiante, imagen_estudiante):
    """
    Guarda la imagen del estudiante en la carpeta correspondiente dentro de Utilidades_db/PHOTO_EST.

    Parámetros:
    - id_estudiante (int): ID del estudiante.
    - imagen_estudiante (UploadedFile): Archivo de imagen subido en Streamlit.

    Retorna:
    - str: Mensaje de éxito o error.
    """
    try:
        if imagen_estudiante is not None:
            path = f"Utilidades_db/PHOTO_EST/{id_estudiante}"
            os.makedirs(path, exist_ok=True)
            imagen_path = os.path.join(path, f"Foto_{id_estudiante}.png")
            image = Image.open(imagen_estudiante)
            image.save(imagen_path)
            return f"✅ Imagen guardada en {imagen_path}."
        else:
            return "⚠️ No se cargó ninguna imagen."
    except Exception as e:
        return f"❌ Error al guardar la imagen: {e}"
    
def obtener_historial_cambios_representantes(ids_estudiantes):
    # Si 'ids_estudiantes' es una Serie de pandas, conviértelo a una lista
    if isinstance(ids_estudiantes, pd.Series):
        ids_estudiantes = ids_estudiantes.tolist()

    # Asegurarse de que `ids_estudiantes` sea una lista o tupla
    if not isinstance(ids_estudiantes, (list, tuple)):
        ids_estudiantes = [ids_estudiantes]

    with db_conector.get_db() as db:
        try:
            historial_cambios = db.query(
                Estudiantes.ID_EST,
                Estudiantes.NOMBRE_EST,
                Estudiantes.APELLIDO_EST,
                Representantes.NOMBRE_REP.label("NOMBRE_REPRE"),
                Representantes.APELLIDO_REP.label("APELLIDO_REPRE"),
                RepreEst.ESTADO,
                RepreEst.RAZON,
                RepreEst.FECHA_CAMBIO,
                RepreEst.CAMBIO_DE
            ).join(Estudiantes, RepreEst.ID_EST == Estudiantes.ID_EST)\
            .join(Representantes, RepreEst.ID_REPRE == Representantes.ID_REP)\
            .filter(Estudiantes.ID_EST.in_(ids_estudiantes))\
            .order_by(RepreEst.FECHA_CAMBIO.desc()).all()
            
            return [row._asdict() for row in historial_cambios]
        except Exception as e:
            print(f"Error al consultar historial de cambios: {e}")
            return None

def obtener_asistencias_por_fecha_y_seccion(fecha_desde, fecha_hasta, seccion_seleccionada=None):
    """
    Obtiene las asistencias de los estudiantes dentro de un rango de fechas y una sección específica (opcional).
    :param fecha_desde: Fecha de inicio del rango
    :param fecha_hasta: Fecha de fin del rango
    :param seccion_seleccionada: Sección específica a filtrar (opcional)
    :return: Lista de registros de asistencias
    """
    try:
        fecha_desde = fecha_desde.date() if isinstance(fecha_desde, datetime.datetime) else fecha_desde
        fecha_hasta = fecha_hasta.date() if isinstance(fecha_hasta, datetime.datetime) else fecha_hasta

        with db_conector.get_db() as db:
            query = db.query(
                AsistenciaEstudiantes.ID_ASISTENCIA_ESTUD,
                Estudiantes.NOMBRE_EST.label("Nombre_Estudiante"),
                Estudiantes.APELLIDO_EST.label("Apellido_Estudiante"),
                Secciones.NOMBRE_SECCION.label("Sección"),
                Grados.NOMBRE_GRADO.label("Grado"),
                (Profesores.NOMBRE_PROF + ' ' + Profesores.APELLIDO_PROF).label("Profesor_A_Cargo"),
                AsistenciaEstudiantes.FECHA_ASISTENCIA,
                AsistenciaEstudiantes.ESTADO_ASISTENCIA,
                AsistenciaEstudiantes.YEAR_ESCOLAR
            ).join(Estudiantes, AsistenciaEstudiantes.ID_EST == Estudiantes.ID_EST)\
            .join(Secciones, AsistenciaEstudiantes.ID_SECCION == Secciones.ID_SECCION)\
            .join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .filter(AsistenciaEstudiantes.FECHA_ASISTENCIA.between(fecha_desde, fecha_hasta))

            if seccion_seleccionada:
                query = query.filter(Secciones.NOMBRE_SECCION == seccion_seleccionada)
            
            asistencias = query.all()
            return [row._asdict() for row in asistencias]

    except Exception as e:
        print(f"Error al obtener asistencias: {e}")
        return None

def obtener_grados():
    """
    Obtiene la lista de grados desde la base de datos.
    """
    with db_conector.get_db() as db:
        try:
            grados = db.query(Grados.ID_GRADOS, Grados.NOMBRE_GRADO).all()
            return grados
        except Exception as e:
            print(f"Error al obtener grados: {e}")
            return []

def obtener_secciones_por_grado(grado_seleccionado):
    """
    Obtiene las secciones para un grado específico desde la base de datos.
    """
    with db_conector.get_db() as db:
        try:
            secciones = db.query(
                Secciones.ID_SECCION,
                Secciones.NOMBRE_SECCION,
                Grados.NOMBRE_GRADO,
                Profesores.NOMBRE_PROF,
                Profesores.APELLIDO_PROF
            ).join(Grados, Secciones.ID_GRADO == Grados.ID_GRADOS)\
            .join(Profesores, Secciones.ID_PROF == Profesores.ID_PROF)\
            .filter(Grados.NOMBRE_GRADO == grado_seleccionado).all()
            
            return [s._asdict() for s in secciones]
        except Exception as e:
            print(f"Error al obtener secciones por grado: {e}")
            return []
