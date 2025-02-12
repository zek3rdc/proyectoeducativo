import openpyxl
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

def rellenar_plantilla_excel(data, plantilla_path, output_path):
    # Eliminar el archivo de salida si ya existe
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Abrir el archivo de la plantilla
    wb = openpyxl.load_workbook(plantilla_path)
    sheet = wb["PZ Nombre de la Institución "]  # Asegúrate de que el nombre de la hoja sea correcto

    # Rellenar los datos en la plantilla
    fila = 12  # Fila inicial

    # Definir las columnas para los cargos
    cargos_columnas = {
        "Profesor": "G",
        "Director": "H",
        "Coordinador": "I",
        "Subdirector": "J",
        "Secretario": "K",
        "Otro": "L"
    }

    # Colocar los nombres de los cargos en la fila combinada G10 a L10
    columna_cargo = 7  # Comenzamos en la columna G
    for cargo, col in cargos_columnas.items():
        sheet[f"{col}10"] = cargo

    for index, prof in enumerate(data, start=1):
        # Fila donde se pondrán los datos
        row = fila + index - 1
        
        # Índice en la columna A
        sheet[f"A{row}"] = index
        
        # Nombres y apellidos en la columna B
        sheet[f"B{row}"] = f"{prof['Nombre']} {prof['Apellido']}"
        
        # Cédula en la columna C
        sheet[f"C{row}"] = prof['Cedula']
        
        # Fecha laboral en la columna E
        fecha_laboral = datetime.strptime(prof['Fecha Laboral'], "%Y-%m-%d")
        dias_laborados = (datetime.now() - fecha_laboral).days
        sheet[f"E{row}"] = dias_laborados
        
        # Cargo (fila G10 a L10, de manera vertical)
        cargos = prof['Cargo']
        # Marcar el cargo correspondiente con una "X"
        for cargo in cargos:
            if cargo in cargos_columnas:
                columna = cargos_columnas[cargo]
                sheet[f"{columna}{row}"] = "X"
        
        # Estudios (Sí/No en las columnas T y U)
        sheet[f"T{row}"] = "X" if prof['Estudios'] == "Sí" else ""
        sheet[f"U{row}"] = "X" if prof['Estudios'] == "No" else ""
        
        # Turno (mañana, tarde, sab-dom en V, W, X)
        if prof['Turno'] == "Mañana":
            sheet[f"V{row}"] = "X"
        elif prof['Turno'] == "Tarde":
            sheet[f"W{row}"] = "X"
        elif prof['Turno'] == "Sab-Dom":
            sheet[f"X{row}"] = "X"
        
        # Grado que atiende en la columna Y
        sheet[f"Y{row}"] = prof['Nivel Grado']
        
        # Codificación (Lic, PG, PGE, TSU, Br.Dc., NG en Z-AA-AE)
        codificacion = prof['Codificacion']
        codificaciones = {"Lic": "Z", "PG": "AA", "PGE": "AB", "TSU": "AC", "Br.Dc.": "AD", "NG": "AE"}
        if codificacion in codificaciones:
            sheet[f"{codificaciones[codificacion]}{row}"] = "X"
        
        # Categoría (I-VI en AF-AK)
        categorias = {
            "I": "AF", "II": "AG", "III": "AH", "IV": "AI", "V": "AJ", "VI": "AK"
        }
        if prof['Categoria'] in categorias:
            sheet[f"{categorias[prof['Categoria']]}{row}"] = "X"
        
        # Número de asistencias en la columna AL
        sheet[f"AL{row}"] = prof['Numero Asistencias']
        
        # Porcentaje de asistencia en la columna AM
        sheet[f"AM{row}"] = prof['Porcentaje Asistencia']
        
        # Número de inasistencias en la columna AN
        sheet[f"AN{row}"] = prof['Numero Inasistencias']
        
        # Porcentaje de inasistencia en la columna AO
        sheet[f"AO{row}"] = prof['Porcentaje Inasistencia']
        
        # Porcentaje de justificadas en la columna AP
        sheet[f"AP{row}"] = prof['Porcentaje Justificadas']
        
        # Porcentaje de injustificadas en la columna AQ
        sheet[f"AQ{row}"] = prof['Porcentaje Injustificadas']
        
        # Número de justificaciones en la columna AU
        sheet[f"AU{row}"] = prof['Numero Justificaciones']

    # Guardar el archivo modificado
    wb.save(output_path)

# Ejemplo de uso
data = [
    {
        "Nombre": "Juan",
        "Apellido": "Pérez",
        "Cedula": 123456789,
        "Fecha Laboral": "2020-01-15",  # Fecha en formato YYYY-MM-DD
        "Cargo": ["Profesor", "Director"],  # Cargo(s) del profesor
        "Estudios": "Sí",
        "Turno": "Mañana",
        "Nivel Grado": "Primero",
        "Codificacion": "Lic",
        "Categoria": "I",
        "Numero Asistencias": 20,
        "Porcentaje Asistencia": 80.0,
        "Numero Inasistencias": 5,
        "Porcentaje Inasistencia": 20.0,
        "Porcentaje Justificadas": 50.0,
        "Porcentaje Injustificadas": 50.0,
        "Numero Justificaciones": 2
    },
    # Añadir más datos según sea necesario
]

plantilla_path = "dependencias/plantillas/5- Enero 2023 -.xlsx"
output_path = "resultado.xlsx"

rellenar_plantilla_excel(data, plantilla_path, output_path)
