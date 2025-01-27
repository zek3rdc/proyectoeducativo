import streamlit as st
import streamlit as st
from modulos.parametros_generales.componente_parametros import (
    obtener_personal_sin_acceso,
    asignar_usuario_a_personal,
    obtener_usuarios,
    editar_usuario,
    eliminar_usuario,
)
from modulos.parametros_generales.componente_parametros import config_manager
from modulos.parametros_generales import componente_parametros
import pandas as pd
import time


# Función para obtener los módulos disponibles dinámicamente
def obtener_modulos_disponibles():
    """
    Retorna una lista de módulos disponibles basados en las importaciones.
    """
    return [
        "Dashboard", "Calificaciones", "Asistencias", "Personal", 
        "Estudiantes", "Materias", "Representantes", "Rendimiento", 
        "Secciones", "Grados", "Parametros Generales"
    ]

# Función principal del módulo de Parámetros Generales
def mostrar():
    st.title("Parámetros Generales")
    opcion = st.sidebar.selectbox("Selecciona una opción", ["Gestión de Roles", "Gestión de Usuarios"])
    if opcion == "Gestión de Roles":
            tabs = st.tabs(["Crear Rol", "Editar Rol", "Eliminar Rol"])
        # Submenú para gestionar la aplicación
        
           
            

            # Obtener módulos disponibles dinámicamente
            modulos_disponibles = obtener_modulos_disponibles()

            with tabs[0]:
                nuevo_rol = st.text_input("Nuevo Rol")
                permisos = st.multiselect("Selecciona los módulos permitidos para este rol", modulos_disponibles)
                submit = st.button("Agregar Rol")
                if submit:
                    if nuevo_rol.lower() == "admin":
                        st.error("No puedes crear un rol llamado 'admin'.")
                    elif nuevo_rol and permisos:
                        mensaje = componente_parametros.agregar_rol(config_manager, nuevo_rol, permisos)
                        st.success(mensaje)
                        time.sleep(2) 
                        st.rerun()
                    else:
                        st.error("El nombre del rol y los módulos no pueden estar vacíos.")

            with tabs[1]:
                roles = list(config_manager.config["roles"].keys())
                rol_actual = st.selectbox("Selecciona un rol para editar", roles)

                if rol_actual.lower() == "admin":
                    st.warning("El rol 'admin' no se puede editar.")
                elif rol_actual.lower() == "sin asignar":
                    st.warning("El rol 'sin asignar' no se puede editar.")
                else:
                    nuevo_rol = st.text_input("Nuevo nombre del rol", rol_actual)
                    permisos = st.multiselect(
                        "Selecciona los módulos permitidos para este rol",
                        modulos_disponibles,
                        default=config_manager.config["roles"][rol_actual]
                    )
                    submit = st.button("Actualizar Rol")
                    if submit:
                        if nuevo_rol and permisos:
                            mensaje = componente_parametros.editar_rol(config_manager, rol_actual, nuevo_rol, permisos)
                            st.success(mensaje)
                            time.sleep(2) 
                            st.rerun()
                        else:
                            st.error("El nombre del rol y los módulos no pueden estar vacíos.")

            with tabs[2]:
                roles = list(config_manager.config["roles"].keys())
                rol_a_eliminar = st.selectbox("Selecciona un rol para eliminar", roles)

                if rol_a_eliminar.lower() == "admin":
                    st.warning("El rol 'admin' no se puede eliminar.")
                elif rol_actual.lower() == "sin asignar":
                    st.warning("El rol 'sin asignar' no se puede eliminar.")
                else:
                    submit = st.button("Eliminar Rol")
                    if submit:
                        mensaje = componente_parametros.eliminar_rol(config_manager, rol_a_eliminar)
                        st.success(mensaje)
                        time.sleep(2) 
                        st.rerun()


                    
    elif opcion == "Gestión de Usuarios":
        st.subheader("Gestión de Usuarios")


        # Crear las pestañas
        tabs = st.tabs(["Crear Usuario", "Ver Usuarios", "Editar Usuario", "Asignar Rol A Usuario"])

        with tabs[0]:
            # Obtener la lista de personal sin acceso
            personal_sin_acceso = obtener_personal_sin_acceso()
            if not personal_sin_acceso:
                st.info("Todos los profesores tienen un ID de acceso asignado.")
            else:
                if personal_sin_acceso:
                    personal = {f"{p['nombre']} {p['apellido']} ({p['cedula']})": p for p in personal_sin_acceso}
                    seleccion = st.selectbox("Selecciona el personal para asignar un usuario", list(personal.keys()))
                    seleccionado = personal[seleccion]

                    # Verificar si el ID de acceso ya existe en el archivo YAML
                    id_acceso_personal = seleccionado.get("id_acceso", "No disponible")
                    
                    if id_acceso_personal != "Sin Asignar" and id_acceso_personal != "No disponible":
                        # Consultar en el archivo YAML si ya existe este ID_ACCESO
                        usuarios = config_manager.config.get("usuarios", {})
                      
                        # Verificar si existe un usuario con el mismo ID de acceso
                        if any(usuario.get("id_acceso") == id_acceso_personal for usuario in usuarios.values()):
                           
                            st.warning(f"El personal {seleccionado['nombre']} {seleccionado['apellido']} ya tiene un usuario asignado.")
                        else:
                            # Proceso para asignar el usuario si no existe
                            username = st.text_input("Nombre de usuario")
                            contrasena = st.text_input("Contraseña", type="password")  # Contraseña personalizada
                            permisos_coordinador = st.checkbox("Asignar rol de coordinador")
                            submit = st.button("Crear Usuario")


                            if submit:
                                if username and contrasena:
                                    # Generar un ID de acceso seguro usando UUID
                                    id_acceso_seguro = componente_parametros.generar_id_acceso_seguro()

                                    mensaje = asignar_usuario_a_personal(
                                        config_manager,
                                        seleccionado["id_profesor"],
                                        seleccionado["nombre"],
                                        seleccionado["apellido"],
                                        seleccionado["cedula"],
                                        username,
                                        contrasena,  # Contraseña proporcionada
                                        id_acceso_seguro,
                                        permisos_coordinador  # Asignar el ID de acceso generado
                                    )
                                    if "exitosamente" in mensaje:
                                        st.success(mensaje)
                                        time.sleep(2) 
                                        st.rerun()
                                    else:
                                        st.error(mensaje)
                                else:
                                    st.error("El nombre de usuario y la contraseña no pueden estar vacíos.")
                    else:
                        st.info(f"El personal {seleccionado['nombre']} {seleccionado['apellido']} aún no tiene un ID de acceso asignado.")
                else:
                    st.info("Todo el personal ya tiene un usuario asignado.")

        with tabs[1]:
            #VER USUARIOS
            st.write("Lista de usuarios registrados:")
            
            try:
                usuarios = obtener_usuarios()
                
                if isinstance(usuarios, dict):  # Aseguramos que obtenemos un diccionario de usuarios
                    # Crear una lista para almacenar los datos de los usuarios
                    lista_usuarios = []
                    
                    for username, info in usuarios.items():
                        lista_usuarios.append({
                            "Usuario": username,
                            "Nombre": info.get('name', 'No disponible'),
                            "Rol: ": info.get('role', 'No disponible'),
                            # Convertir 'Cédula' a int si es posible, si no, dejar "No disponible"
                            "Cordinador ": info.get('coordinate', 'No disponible'),
                            "Cédula": str(info.get('cedula', 'No disponible')),  # Aseguramos que sea una cadena
                            "ID Profesor": info.get('id_profesor', 'No disponible'),
                            "ID Acceso": info.get('ID_ACCESO', 'No disponible')  # Mostrar el ID de acceso
                        })
                    
                    # Crear un DataFrame con la lista de usuarios
                    df_usuarios = pd.DataFrame(lista_usuarios)
                    
                    # Asegurarnos de convertir 'Cédula' a un tipo numérico (si es posible)
                    df_usuarios["Cédula"] = pd.to_numeric(df_usuarios["Cédula"], errors='coerce').fillna("No disponible").astype(str)
                    
                    # Mostrar el DataFrame como una tabla
                    st.dataframe(df_usuarios)

                    # Seleccionar un usuario para ver más detalles
                    seleccion = st.selectbox("Selecciona un usuario para ver más detalles:", df_usuarios["Usuario"].tolist())
                    
                    if seleccion:
                        # Obtener la información del usuario seleccionado
                        usuario_info = usuarios[seleccion]
                        
                        # Obtener el ID_ACCESO del usuario seleccionado
                        id_acceso = usuario_info.get("ID_ACCESO", None)
                        
                        # Mostrar detalles del usuario seleccionando su ID_ACCESO
                        if id_acceso:
                            detalles_usuario = componente_parametros.obtener_detalles_usuario(id_acceso)
                            if detalles_usuario:
                                # Crear una segunda tabla con los detalles
                                df_detalles = pd.DataFrame([detalles_usuario])
                                st.write(f"Detalles del usuario {seleccion} (ID Acceso: {id_acceso}):")
                                st.dataframe(df_detalles)
                            else:
                                st.warning(f"No se encontraron detalles para el ID Acceso {id_acceso}.")
                        else:
                            st.warning(f"El usuario {seleccion} no tiene un ID Acceso asignado.")
                else:
                    st.info("No hay usuarios registrados.")
            except Exception as e:
                st.error(f"Error al cargar los usuarios: {e}")

        with tabs[2]:
            # EDITAR USUARIOS
            # Obtener la lista de usuarios existentes
            usuarios = obtener_usuarios()
            
            if usuarios:
                # Sección para editar usuarios
                st.subheader("Editar Usuario")
                username_a_editar = st.selectbox("Selecciona el usuario a editar", list(usuarios.keys()))
                usuario_info = usuarios[username_a_editar]

                # Campos para editar
                nuevo_username = st.text_input("Nuevo Nombre de Usuario", value=username_a_editar)
                nueva_contrasena = st.text_input("Nueva Contraseña", type="password")
                coordinate_new = st.checkbox("Nuevo Coordinador?")

                submit = st.button("Actualizar Usuario")

                if submit:
                    if nuevo_username and nueva_contrasena:
                        mensaje = editar_usuario(
                            config_manager,
                            usuario_info["id_acceso"],
                            nuevo_username,
                            nueva_contrasena,
                            coordinate_new  # Solo se actualizará si la contraseña es proporcionada
                        )
                        if "exitosamente" in mensaje:
                            st.success(mensaje)
                            time.sleep(2) 
                            st.rerun()
                        else:
                            st.error(mensaje)
                    else:
                        st.error("Debe proporcionar un nuevo nombre de usuario y contraseña.")
                
                # Sección para eliminar usuarios
                st.subheader("Eliminar Usuario")
                usernames_a_eliminar = st.multiselect("Selecciona los usuarios a eliminar", list(usuarios.keys()))

                eliminar_submit = st.button("Eliminar Usuarios")

                if eliminar_submit:
                    if usernames_a_eliminar:
                        mensajes_eliminar = []
                        for username in usernames_a_eliminar:
                            # Verificar si el usuario es un admin
                            if usuarios[username]["role"] == "admin":
                                mensajes_eliminar.append(f"No se puede eliminar al usuario {username} porque tiene rol de admin.")
                            else:
                                mensaje_eliminar = eliminar_usuario(config_manager, usuarios[username]["id_acceso"])
                                mensajes_eliminar.append(mensaje_eliminar)

                        for mensaje in mensajes_eliminar:
                            if "exitosamente" in mensaje:
                                st.success(mensaje)
                            else:
                                st.error(mensaje)
                        time.sleep(2) 
                        st.rerun()  # Recargar la aplicación para reflejar los cambios
                    else:
                        st.warning("No has seleccionado ningún usuario para eliminar.")


        with tabs[3]:
            st.subheader("Asignar Rol a un Usuario Existente")

            # Obtener la lista de usuarios desde el archivo YAML
            usuarios = obtener_usuarios()
            
            if usuarios:
                # Mostrar un selectbox para elegir el usuario a modificar
                username_a_modificar = st.selectbox("Selecciona el usuario a asignar un rol", list(usuarios.keys()))
                usuario_info = usuarios[username_a_modificar]

                # Mostrar el rol actual del usuario
                st.write(f"Rol actual de {username_a_modificar}: {usuario_info.get('role', 'No asignado')}")

                # Obtener los roles predefinidos del archivo YAML
                roles_disponibles = config_manager.config.get("roles", {}).keys()

                # Selección de nuevo rol para el usuario
                nuevo_rol = st.selectbox("Selecciona el nuevo rol", list(roles_disponibles))

                # Mostrar las opciones disponibles para ese rol
                st.write(f"Permisos del rol '{nuevo_rol}':")
                permisos = config_manager.config.get("roles", {}).get(nuevo_rol, [])

                # Verificar si la lista de permisos está vacía
                if permisos:
                    st.write(", ".join(permisos))
                else:
                    st.write("Este rol no tiene permisos definidos.")

                submit = st.button("Actualizar Rol")

                if submit:
                    # Llamar a la función para actualizar el rol
                    mensaje = componente_parametros.asignar_rol_usuario(config_manager, usuarios, username_a_modificar, nuevo_rol)
                    if "Error" in mensaje:
                        st.error(mensaje)
                    else:
                        st.success(mensaje)
                        time.sleep(2)
                        st.rerun()
            else:
                st.info("No hay usuarios registrados para asignar un rol.")
