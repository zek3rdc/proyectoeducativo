import streamlit as st
from modulos.Utilidades.FuncionesGenerales import subHeader

def dashboard():

    subHeader('Compras por Proveedor', divider='rainbow',)

def mostrar():
    st.header("Módulo de Calificaciones")
    st.write("Aquí se gestionarán las calificaciones de los estudiantes.")
