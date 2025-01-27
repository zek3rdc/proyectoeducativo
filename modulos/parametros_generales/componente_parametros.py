import streamlit as st
from dependencias.security.config_manager import ConfigManager
import bcrypt
import yaml
from modulos.db_conector import obtener_datos, ejecutar_query, insertar_id_acceso_en_base_de_datos,conectar
import uuid
import os
from dependencias.security.config_manager import ConfigManager
import pandas as pd





# Ruta al archivo de configuración YAML
config_path = "config.yaml"

# Inicializa el ConfigManager
config_manager = ConfigManager(config_path)

# Funciones para gestionar roles
def agregar_rol(config_manager, rol, permisos):
    config = config_manager.config
    if rol not in config["roles"]:
        config["roles"][rol] = permisos
        config_manager.save_config()
        return f"Rol '{rol}' agregado exitosamente."
    else:
        return f"El rol '{rol}' ya existe."

def editar_rol(config_manager, rol, nuevo_rol, permisos):
    config = config_manager.config
    if rol in config["roles"]:
        del config["roles"][rol]  # Eliminar el rol antiguo
        config["roles"][nuevo_rol] = permisos  # Agregar el nuevo rol
        config_manager.save_config()
        return f"Rol '{rol}' actualizado a '{nuevo_rol}' exitosamente."
    else:
        return f"El rol '{rol}' no existe."

def eliminar_rol(config_manager, rol):
    config = config_manager.config
    if rol in config["roles"]:
        del config["roles"][rol]
        config_manager.save_config()
        return f"Rol '{rol}' eliminado exitosamente."
    else:
        return f"El rol '{rol}' no existe."

# Función para obtener personal sin acceso
def obtener_personal_sin_acceso():
    """
    Obtiene el personal sin ID de acceso asignado.
    """
    query = """
    SELECT 
        p."ID_PROF" AS id_profesor,
        p."NOMBRE_PROF" AS nombre,
        p."APELLIDO_PROF" AS apellido,
        p."CEDULA_PROF" AS cedula,
        CASE 
            WHEN p."ID_ACCESO" IS NULL THEN 'Sin Asignar'
            ELSE p."ID_ACCESO"::TEXT
        END AS id_acceso
    FROM 
        public."PROFESORES" p
    ORDER BY 
        p."NOMBRE_PROF";
    """
    return ejecutar_query(query)


# Función para asignar un usuario a un profesor



def asignar_usuario_a_personal(config_manager, id_profesor, nombre, apellido, cedula, username, contrasena, id_acceso,coordinate):
    """
    Asocia un nombre de usuario a un profesor y lo registra en un sistema de autenticación.
    El campo ID_ACCESO en la base de datos es UUID, por lo que se genera un UUID único.
    """
    try:
        # Hashear la contraseña
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        # Generar un UUID para ID_ACCESO si es necesario
        id_acceso = str(uuid.uuid4())  # Generar un UUID único como cadena

        # Asegúrate de que la ruta sea correcta
        archivo_yml = config_manager.path  # Usamos la ruta que has definido

        # Verifica si el archivo existe antes de intentar abrirlo
        if not os.path.exists(archivo_yml):
            return f"El archivo de configuración {archivo_yml} no se encuentra."

        # Cargar la configuración del archivo YAML
        with open(archivo_yml, "r") as file:    
            config = yaml.safe_load(file) or {}

        # Asegurarse de que la clave 'credentials' y 'usernames' existen
        if "credentials" not in config:
            config["credentials"] = {}
        if "usernames" not in config["credentials"]:
            config["credentials"]["usernames"] = {}

        # Agregar el nuevo usuario bajo 'credentials.usernames'
        config["credentials"]["usernames"][username] = {
            "email": cedula,  # Asumimos que 'cedula' se usa como email en este caso
            "failed_login_attempts": 0,
            "logged_in": False,
            "name": f"{nombre} {apellido}",
            "password": contrasena_hash.decode('utf-8'),  # Guardar la contraseña hasheada
            "role": "Sin Asignar",  # Aquí puedes cambiar el rol según sea necesario
            "username": username,
            "id_acceso": id_acceso ,
            "coordinate": coordinate # Asignar el UUID generado como ID_ACCESO
        }

        # Guardar los cambios en el archivo YAML
        with open(archivo_yml, "w") as file:
            yaml.dump(config, file)

        # Ahora insertar o actualizar el ID_ACCESO en la base de datos si es necesario
        # (Esto depende de cómo estés gestionando los usuarios en la base de datos)
        # Aquí va el código para insertar el ID_ACCESO en la base de datos
        mensaje_db = insertar_id_acceso_en_base_de_datos(id_profesor, id_acceso)  # Esta función debes implementarla para hacer la inserción

        if "exitosamente" in mensaje_db:
            return f"Usuario {username} asignado exitosamente con ID de acceso {id_acceso}."
        else:
            return f"Error al asignar ID de acceso en la base de datos: {mensaje_db}"

    except Exception as e:
        return f"Error al asignar el usuario: {e}"





# Función para obtener usuarios registrados
def obtener_usuarios():
    """
    Obtiene la lista de usuarios registrados en el archivo YAML, incluyendo su ID de acceso.
    """
    try:
        # Cargar configuración desde el archivo YAML
        config_path = os.getcwd() + '/config.yaml'
        with open(config_path) as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)

        # Acceder correctamente a los usuarios dentro de 'credentials.usernames'
        usuarios = config.get("credentials", {}).get("usernames", {})
        
        # Si los usuarios están correctamente cargados, retornamos la lista
        if usuarios:
            # Agregar el ID_ACCESO (si está disponible) en la información de cada usuario
            for username, info in usuarios.items():
                info["ID_ACCESO"] = info.get("id_acceso", "No disponible")
            return usuarios
        else:
            return "No se encontraron usuarios en el archivo YAML."
    except Exception as e:
        return f"Error al obtener los usuarios: {e}"





# Función para editar un usuario (username, contraseña o ID de acceso)
def editar_usuario(config_manager, id_profesor, nuevo_username, nueva_contrasena,coordinate):
    """
    Permite editar los detalles de un usuario, actualizando el nombre de usuario,
    la contraseña y el ID_PROFESOR en el archivo YML.
    """
    try:
        # Ruta del archivo YAML
        archivo_yml = os.getcwd() + '/config.yaml'

        # Leer el archivo YAML
        with open(archivo_yml, "r") as file:
            config = yaml.safe_load(file) or {}

        # Acceder a los usuarios dentro de 'credentials.usernames'
        usuarios = config.get("credentials", {}).get("usernames", {})

        # Buscar al usuario actual por su ID_PROFESOR
        usuario_actual = None
        for username, info in usuarios.items():
            if info.get("id_acceso") == id_profesor:
                usuario_actual = username
                break

        if not usuario_actual:
            return f"No se encontró ningún usuario con ID_PROFESOR: {id_profesor}"

        # Si se proporciona una nueva contraseña, hashearla
        if nueva_contrasena:
            contrasena_hash = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            contrasena_hash = usuarios[usuario_actual].get("password")  # Mantener la contraseña actual

        # Actualizar los datos del usuario
        if nuevo_username != usuario_actual:  # Si cambia el nombre de usuario
            usuarios[nuevo_username] = usuarios.pop(usuario_actual)  # Renombrar clave

        usuarios[nuevo_username]["id_acceso"] = id_profesor
        usuarios[nuevo_username]["password"] = contrasena_hash
        usuarios[nuevo_username]["coordinate"] = coordinate

        # Guardar los cambios en el archivo YAML
        with open(archivo_yml, "w") as file:
            yaml.dump(config, file)

        return f"Usuario {nuevo_username} actualizado exitosamente."
    except Exception as e:
        return f"Error al actualizar el usuario: {e}"


def asignar_usuario_a_profesor(config_manager, id_profesor, username, contrasena, role="profesor"):
    """
    Asocia un nombre de usuario y contraseña a un profesor que no tiene ID_ACCESO,
    lo registra en la base de datos y lo agrega al archivo YAML.
    """
    try:
        # Hashear la contraseña
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Verificar que el profesor no tenga ya un ID_ACCESO
        query = """
        SELECT "ID_ACCESO" FROM public."PROFESORES" WHERE "ID_PROF" = %s
        """
        id_acceso = ejecutar_query(query, params=(id_profesor,), fetch=True)

        if id_acceso:
            return f"El profesor ya tiene un ID de acceso asignado."

        # Asignar un nuevo ID_ACCESO (aquí generamos uno nuevo o puedes obtenerlo de otro modo)
        nuevo_id_acceso = generar_id_acceso_seguro()

        # Actualizar la base de datos con el nuevo ID_ACCESO
        query = """
        UPDATE public."PROFESORES"
        SET "ID_ACCESO" = %s
        WHERE "ID_PROF" = %s
        """
        params = (nuevo_id_acceso, id_profesor)
        ejecutar_query(query, params)

        # Registrar al usuario en el archivo YAML
        archivo_yml = config_manager.config[config_path]
        with open(archivo_yml, "r") as file:
            usuarios = yaml.safe_load(file) or {}

        # Agregar el nuevo usuario
        usuarios["credentials"]["usernames"][username] = {
            "email": f"{username}@empresa.com",  # Aquí puedes modificar según sea necesario
            "failed_login_attempts": 0,
            "logged_in": False,
            "name": username,
            "password": contrasena_hash,
            "role": role,
            "username": username
        }

        # Guardar el archivo YAML actualizado
        with open(archivo_yml, "w") as file:
            yaml.dump(usuarios, file)

        return f"Usuario {username} asignado exitosamente al profesor con ID {id_profesor}."
    except Exception as e:
        return f"Error al asignar el usuario: {e}"





def generar_id_acceso_seguro():
    # Genera un UUID único para el ID de acceso
    return str(uuid.uuid4())  # Devuelve el UUID como un string


def obtener_detalles_usuario(id_acceso):
    """
    Obtiene los detalles del usuario desde la base de datos usando su ID_ACCESO.
    """
    try:
        # Conectar a la base de datos
        connection = conectar()
        if connection:
            with connection.cursor() as cursor:
                query = """
                SELECT "NOMBRE_PROF", "APELLIDO_PROF", "CEDULA_PROF", "DIRECCION_PROF", "TELEFONO_PROF", "EMAIL_PROF"
                FROM "PROFESORES"
                WHERE "ID_ACCESO" = %s;
                """
                cursor.execute(query, (id_acceso,))
                detalle = cursor.fetchone()
                
                if detalle:
                    # Asegurar que todos los valores alfanuméricos sean cadenas
                    return {
                        "Nombre": str(detalle[0]) if detalle[0] else "No disponible",
                        "Apellido": str(detalle[1]) if detalle[1] else "No disponible",
                        "Cédula": str(detalle[2]) if detalle[2] else "No disponible",
                        "Dirección": str(detalle[3]) if detalle[3] else "No disponible",
                        "Teléfono": str(detalle[4]) if detalle[4] else "No disponible",
                        "Email": str(detalle[5]) if detalle[5] else "No disponible"
                    }
                else:
                    return None
        else:
            raise Exception("No se pudo conectar a la base de datos.")
    except Exception as e:
        # Si ocurre un error, lo mostramos en Streamlit
        st.error("Usuario no tiene personal asignado")
        return None
def eliminar_usuario(config_manager, id_acceso):
    """
    Permite eliminar un usuario del archivo YML.
    """
    try:
        # Ruta del archivo YAML
        archivo_yml = os.getcwd() + '/config.yaml'

        # Leer el archivo YAML
        with open(archivo_yml, "r") as file:
            config = yaml.safe_load(file) or {}

        # Acceder a los usuarios dentro de 'credentials.usernames'
        usuarios = config.get("credentials", {}).get("usernames", {})

        # Buscar al usuario por su ID_ACCESO y eliminarlo
        usuario_a_eliminar = None
        for username, info in usuarios.items():
            if info.get("id_acceso") == id_acceso:
                usuario_a_eliminar = username
                break

        if not usuario_a_eliminar:
            return f"No se encontró ningún usuario con ID_ACCESO: {id_acceso}"

        # Eliminar el usuario del diccionario
        del usuarios[usuario_a_eliminar]

        # Guardar los cambios en el archivo YAML
        with open(archivo_yml, "w") as file:
            yaml.dump(config, file)

        return f"Usuario {usuario_a_eliminar} eliminado exitosamente."
    except Exception as e:
        return f"Error al eliminar el usuario: {e}"




def asignar_rol_usuario(config_manager, usuarios, username_a_modificar, nuevo_rol):
    """
    Asigna un nuevo rol a un usuario y actualiza el archivo YAML.
    
    Args:
        config_manager: Instancia de ConfigManager para acceder y guardar la configuración.
        usuarios (dict): Diccionario de usuarios cargado desde el archivo YAML.
        username_a_modificar (str): Nombre de usuario al que se le asignará el nuevo rol.
        nuevo_rol (str): El nuevo rol a asignar al usuario.
        
    Returns:
        str: Mensaje de éxito o error.
    """
    try:
        usuario_info = usuarios[username_a_modificar]
        
        # Asignar el nuevo rol al usuario
        usuario_info["role"] = nuevo_rol
        usuarios[username_a_modificar] = usuario_info  # Guardar los cambios en el usuario

        # Actualizar los usuarios en la configuración
        config_manager.config["credentials"]["usernames"] = usuarios
        config_manager.save()  # Guardar el archivo actualizado
        
        # Obtener los permisos del rol
        permisos = config_manager.config.get("roles", {}).get(nuevo_rol, [])
        
        # Devolver el mensaje de éxito
        return f"El rol de {username_a_modificar} se ha actualizado a {nuevo_rol} con permisos: {', '.join(permisos)}."
    except Exception as e:
        return f"Error al actualizar el rol del usuario: {str(e)}"
