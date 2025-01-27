import streamlit as st
from modulos.Utilidades.FuncionesGenerales import subHeader
from modulos.main_Componentes import componentes_profesores
from modulos import db_conector
from modulos.CrearTablas import crear_dataframe
import datetime



def dashboard():

    subHeader('Compras por Proveedor', divider='rainbow',)

def mostrar():
    st.header("Módulo de Personal")
    
    # Opciones en el sidebar
    st.sidebar.title("Opciones de Personal")
    opcion = st.sidebar.radio("Selecciona una acción", ["Listar", "Agregar", "Editar", "Eliminar", "Gestionar Roles"])

    if opcion == "Listar":
        st.subheader("Lista de Personal")
        profesores = db_conector.listar_profesores()
        if not profesores:
            st.warning("No hay personal registrados.")
        else:
            # Aquí se muestra la tabla con todos los profesores, incluyendo los que no tienen rol
            df = crear_dataframe(profesores)
            st.table(df)

    elif opcion == "Agregar":
        st.subheader("Agregar Nuevo personal")
        with st.form("form_agregar_profesor"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            fecha_nac = st.date_input(
    "Fecha de Nacimiento",
    min_value=datetime.date(1900, 1, 1),  # Fecha mínima (1 de enero de 1900)
    max_value=datetime.date.today()  # Fecha máxima (hoy)
)
            cedula = st.text_input("Cédula")
            email = st.text_input("Email")
            telefono = st.text_input("Teléfono")
            direccion = st.text_input("Dirección")
            codificacion = st.selectbox("Codificación" , ["Lic.", "PG", "PGE","TSU","Br.Dc","NG"])
            categoria = st.selectbox("Categoría" , ["I","II","III","IV","V","VI"])
            estudios = st.selectbox("Estudia Actual" , ["Si","No"])
            fecha_job = st.date_input("Desde Cuando Labora?")
            
            # Obtener los roles disponibles de la base de datos, incluyendo el rol 'Sin Rol'
            roles = componentes_profesores.listar_roles()  # Obtener roles desde la tabla de roles
            roles.append("Sin Rol")  # Añadir opción para 'Sin Rol'
            
            rol = st.selectbox("Rol", roles)  # Selección de rol

            submit = st.form_submit_button("Agregar")
            if submit:
                if nombre and apellido and cedula and email and telefono and direccion and rol:
                    componentes_profesores.agregar_profesor(nombre, apellido, fecha_nac,cedula, email, telefono, direccion, codificacion,categoria,estudios,fecha_job, rol)
                    st.success("Profesor agregado exitosamente.")
                else:
                    st.error("Todos los campos son obligatorios.")

    elif opcion == "Editar":
        st.subheader("Editar Personal")
        profesores = db_conector.listar_profesores()
        if not profesores:
            st.warning("No hay personal registrados.")
        else:
            # Mostrar la tabla de profesores
            df = crear_dataframe(profesores)
            st.table(df)

            # Selección del profesor a editar
            ids = [prof["id_profesor"] for prof in profesores]
            id_profesor = st.selectbox("Selecciona un personal para editar", ids)
            profesor = next(prof for prof in profesores if prof["id_profesor"] == id_profesor)

            # Formulario para editar los datos del profesor
            with st.form("form_editar_profesor"):
                nombre = st.text_input("Nombre", profesor["nombre"])
                apellido = st.text_input("Apellido", profesor["apellido"])
                fecha_nac = st.date_input(
    "Fecha de Nacimiento",
    profesor["fecha_nacimiento"],  # Fecha por defecto del profesor
    min_value=datetime.date(1900, 1, 1),  # Fecha mínima (1 de enero de 1900)
    max_value=datetime.date.today()  # Fecha máxima (hoy)
)

                cedula = st.text_input("Cédula", profesor["cedula"])
                email = st.text_input("Email", profesor["email"])
                telefono = st.text_input("Teléfono", profesor["telefono"])
                direccion = st.text_input("Dirección", profesor["direccion"])
                codificacion = st.selectbox("Codificación" , ["Lic.", "PG", "PGE","TSU","Br.Dc","NG"])
                categoria = st.selectbox("Categoría" , ["I","II","III","IV","V","VI"])
                estudios = st.selectbox("Estudia Actual" , ["Si","No"])
                fecha_job = st.date_input("Desde Cuando Labora?", profesor["fecha_laboral"])

                
                # Obtener los roles disponibles de la base de datos, incluyendo 'Sin Rol'
                roles = componentes_profesores.listar_roles()  # Obtener roles desde la tabla de roles
                roles.append("Sin Rol")  # Añadir opción para 'Sin Rol'
                
                rol = st.selectbox("Rol", roles, index=roles.index(profesor["rol"]))  # Seleccionar el rol actual

                submit = st.form_submit_button("Guardar Cambios")
                if submit:
                    if nombre and apellido and cedula and email and telefono and direccion and rol:
                        componentes_profesores.editar_profesor(
                            id_profesor, nombre, apellido,fecha_nac, cedula, email, telefono, direccion,codificacion,categoria,estudios,fecha_job, rol
                        )
                        st.success("Profesor actualizado exitosamente.")
                    else:
                        st.error("Todos los campos son obligatorios.")

    elif opcion == "Eliminar":
        st.subheader("Eliminar Personal")
        profesores = db_conector.listar_profesores()
        if not profesores:
            st.warning("No hay profesores registrados.")
        else:
            df = crear_dataframe(profesores)
            st.table(df)
            ids = [prof["id_profesor"] for prof in profesores]
            id_profesor = st.selectbox("Selecciona un profesor para eliminar", ids)
            submit = st.button("Eliminar")
            if submit:
                componentes_profesores.eliminar_profesor(id_profesor)
                st.success("Profesor eliminado exitosamente.")

    elif opcion == "Gestionar Roles":
        st.subheader("Gestionar Roles")
        subopcion = st.radio("Selecciona una acción", ["Crear Rol", "Editar Rol", "Eliminar Rol"])

        if subopcion == "Crear Rol":
            st.subheader("Crear Nuevo Rol")
            with st.form("form_crear_rol"):
                nuevo_rol = st.text_input("Nombre del nuevo rol")
                submit = st.form_submit_button("Crear Rol")
                if submit:
                    if nuevo_rol:
                        # Insertar el nuevo rol en la base de datos
                        componentes_profesores.agregar_rol(nuevo_rol)
                        st.success(f"Rol '{nuevo_rol}' creado exitosamente.")
                    else:
                        st.error("El nombre del rol no puede estar vacío.")

        elif subopcion == "Editar Rol":
            st.subheader("Editar Rol Existente")
            
            # Listar los roles disponibles
            roles = componentes_profesores.listar_roles()
            
            # Selección del rol actual para editar
            rol_actual = st.selectbox("Selecciona un rol para editar", roles)
            
            nuevo_rol = st.text_input("Nuevo nombre del rol", rol_actual)
            
            submit = st.button("Actualizar Rol")
            if submit:
                if nuevo_rol:
                    # Asegúrate de que el nuevo rol sea un valor simple, no un diccionario
                    componentes_profesores.editar_rol(rol_actual, nuevo_rol)
                    st.success(f"Rol '{rol_actual}' actualizado a '{nuevo_rol}' exitosamente.")
                else:
                    st.error("El nombre del rol no puede estar vacío.")


        elif subopcion == "Eliminar Rol":
            st.subheader("Eliminar Rol")
            roles = componentes_profesores.listar_roles()
            rol_a_eliminar = st.selectbox("Selecciona un rol para eliminar", roles)
            submit = st.button("Eliminar Rol")
            if submit:
                componentes_profesores.eliminar_rol(rol_a_eliminar)
                st.success(f"Rol '{rol_a_eliminar}' eliminado exitosamente.")
