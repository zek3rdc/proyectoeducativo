import yaml
from yaml.loader import SafeLoader
import bcrypt
import uuid



class ConfigManager:
    """
    Clase para gestionar la configuración desde un archivo YAML.
    """

    def __init__(self, path):
        """
        Inicializa la clase y carga el archivo YAML.
        
        Args:
            path (str): Ruta al archivo YAML de configuración.
        """
        self.path = path
        self.config = self._load_config(path)

    def _load_config(self, path):
        """
        Carga el archivo YAML de configuración.
        
        Args:
            path (str): Ruta al archivo YAML.

        Returns:
            dict: Configuración cargada como un diccionario.
        """
        try:
            with open(path, "r") as file:
                return yaml.load(file, Loader=SafeLoader)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de configuración no se encontró: {path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error al cargar el archivo YAML: {e}")

    def save_config(self):
        """
        Guarda la configuración actual en el archivo YAML.
        """
        try:
            with open(self.path, "w") as file:
                yaml.dump(self.config, file)
        except Exception as e:
            raise IOError(f"Error al guardar la configuración: {e}")

    def hash_password(self, password):
        """
        Hashea una contraseña usando bcrypt.
        
        Args:
            password (str): Contraseña en texto plano.

        Returns:
            str: Contraseña hasheada.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def assign_user(self, username, nombre, apellido, cedula, id_profesor, password):
        """
        Asigna un nuevo usuario y lo guarda en el archivo YAML.
        
        Args:
            username (str): Nombre de usuario.
            nombre (str): Nombre del profesor.
            apellido (str): Apellido del profesor.
            cedula (str): Cédula del profesor.
            id_profesor (str): ID del profesor.
            password (str): Contraseña en texto plano.

        Returns:
            str: Mensaje de éxito o error.
        """
        try:
            # Generar un UUID para el ID_ACCESO
            id_acceso = str(uuid.uuid4())  # Generar un UUID único como cadena
            
            # Hashear la contraseña
            hashed_password = self.hash_password(password)

            # Verificar si el usuario ya existe
            if username in self.config["usuarios"]:
                return f"El usuario '{username}' ya existe."

            # Crear el nuevo usuario
            self.config["usuarios"][username] = {
                "nombre": nombre,
                "apellido": apellido,
                "cedula": cedula,
                "id_profesor": id_profesor,
                "id_acceso": id_acceso,  # Asignar el UUID generado como ID_ACCESO
                "contrasena": hashed_password
            }

            # Guardar la configuración
            self.save_config()
            return f"Usuario '{username}' asignado exitosamente."

        except Exception as e:
            return f"Error al asignar el usuario: {e}"

    def edit_user(self, username, nuevo_username=None, nueva_contrasena=None, nuevo_id_acceso=None):
        """
        Edita los detalles de un usuario en el archivo YAML.
        
        Args:
            username (str): Nombre de usuario actual.
            nuevo_username (str): Nuevo nombre de usuario (opcional).
            nueva_contrasena (str): Nueva contraseña en texto plano (opcional).
            nuevo_id_acceso (str): Nuevo ID de acceso (opcional).

        Returns:
            str: Mensaje de éxito o error.
        """
        try:
            # Verificar si el usuario existe
            if username not in self.config["usuarios"]:
                return f"El usuario '{username}' no existe."

            # Actualizar el nombre de usuario
            if nuevo_username:
                self.config["usuarios"][nuevo_username] = self.config["usuarios"].pop(username)
                username = nuevo_username

            # Actualizar la contraseña
            if nueva_contrasena:
                hashed_password = self.hash_password(nueva_contrasena)
                self.config["usuarios"][username]["contrasena"] = hashed_password

            # Actualizar el ID de acceso si se proporciona
            if nuevo_id_acceso:
                self.config["usuarios"][username]["id_acceso"] = nuevo_id_acceso  # Actualizar a un nuevo UUID si se proporciona

            # Guardar la configuración
            self.save_config()
            return f"Usuario '{username}' actualizado exitosamente."

        except Exception as e:
            return f"Error al editar el usuario: {e}"


    def delete_user(self, username):
        """
        Elimina un usuario del archivo YAML.
        
        Args:
            username (str): Nombre de usuario a eliminar.

        Returns:
            str: Mensaje de éxito o error.
        """
        try:
            # Verificar si el usuario existe
            if username not in self.config["usuarios"]:
                return f"El usuario '{username}' no existe."

            # Eliminar el usuario
            del self.config["usuarios"][username]

            # Guardar la configuración
            self.save_config()
            return f"Usuario '{username}' eliminado exitosamente."

        except Exception as e:
            return f"Error al eliminar el usuario: {e}"
        
    def update_user(self, username, id_profesor, nueva_contrasena, nuevo_id_acceso):
        """
        Actualiza los detalles de un usuario en el archivo YAML, incluyendo su nombre de usuario (ID_ACCESO),
        la contraseña y el ID del profesor.
        """
        try:
            # Asegurarse de que la clave 'usuarios' existe en la configuración
            if "usuarios" not in self.config:
                self.config["usuarios"] = {}

            # Verificar si el usuario existe
            if username not in self.config["usuarios"]:
                return f"El usuario {username} no existe en el archivo YML."

            # Hashear la nueva contraseña si se proporciona
            if nueva_contrasena:
                contrasena_hash = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
                contrasena_hash = contrasena_hash.decode('utf-8')
            else:
                contrasena_hash = None

            # Actualizar los datos del usuario
            self.config["usuarios"][username]["id_profesor"] = id_profesor
            if contrasena_hash:
                self.config["usuarios"][username]["contrasena"] = contrasena_hash
            if nuevo_id_acceso:
                self.config["usuarios"][username]["id_acceso"] = nuevo_id_acceso  # Usar el nuevo UUID si se proporciona

            # Guardar los cambios en el archivo YAML
            self.save_config()

            return f"Usuario {username} actualizado exitosamente."
        except Exception as e:
            return f"Error al actualizar el usuario en el archivo YML: {e}"

        
    def update_passwords(self):
        """
        Hashea las contraseñas almacenadas en la configuración si no están hasheadas.
        """
        usernames = self.config.get("credentials", {}).get("usernames", {})
        for username, user_data in usernames.items():
            plain_password = user_data.get("password")
            if plain_password and not plain_password.startswith("$2b$"):
                hashed_password = self.hash_password(plain_password)
                self.config["credentials"]["usernames"][username]["password"] = hashed_password
        self.save_config()

    def verify_password(self, plain_password, hashed_password):
        """
        Verifica si una contraseña coincide con su hash.
        
        Args:
            plain_password (str): Contraseña en texto plano.
            hashed_password (str): Contraseña hasheada.

        Returns:
            bool: True si coinciden, False de lo contrario.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def get(self, key, default=None):
        """
        Obtiene un valor de la configuración usando una clave jerárquica.
        
        Args:
            key (str): Clave jerárquica separada por puntos (e.g., "credentials.usernames").
            default (Any): Valor predeterminado si la clave no existe.

        Returns:
            Any: Valor de la configuración o el valor predeterminado.
        """
        keys = key.split('.')
        data = self.config
        for k in keys:
            data = data.get(k, {})
        return data or default