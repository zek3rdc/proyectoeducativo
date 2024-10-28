import streamlit as st
from modulos.Asistencias import asistencias
from modulos.Calificaciones import calificaciones
from modulos.Estudiantes import estudiantes
from modulos.Profesores import profesores
from modulos.Rendimiento import rendimiento
from modulos.secciones import secciones

# Agregar un logo en la parte superior
st.sidebar.image("logo.png", width=150)  # El archivo logo.png debe estar en la misma carpeta del script o proporciona la ruta

# Configurar el título de la aplicación
st.title("Sistema de Gestión Académica")

# Crear el menú de navegación
menu = ["Dashboard", "Calificaciones", "Horarios", "Asistencias", "Profesores", "Estudiantes", "Rendimiento", "Eventos", "Secciones"]
opcion = st.sidebar.selectbox("Selecciona el módulo", menu)

# Dashboard general (en blanco)
if opcion == "Dashboard":
    st.header("Dashboard General")
    st.write("Este es el dashboard en blanco. Puedes navegar a otros módulos usando el menú.")

# Navegar entre módulos
elif opcion == "Calificaciones":
    calificaciones.mostrar()

elif opcion == "Asistencias":
    asistencias.mostrar()

elif opcion == "Profesores":
    profesores.mostrar()

elif opcion == "Estudiantes":
    estudiantes.mostrar()

elif opcion == "Rendimiento":
    rendimiento.mostrar()

elif opcion == "Secciones":
    secciones.mostrar()


