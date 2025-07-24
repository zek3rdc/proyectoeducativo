import sys
import pyodbc
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Verificar que se haya pasado el número de factura como argumento
if len(sys.argv) < 2:
    print("Error: No se proporcionó un número de factura.")
    sys.exit(1)

# Obtener el número de factura desde VBA
numero_factura = sys.argv[1]

# Conectar a Access
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Database2.accdb;READONLY=1;')
cursor = conn.cursor()

# Obtener los datos de la factura
cursor.execute(f"""
    SELECT 
        F.NumeroFactura, F.FechaEmision, C.Nombre, C.Cedula, C.RIF, 
        P.Nombre, DV.Cantidad, DV.Precio, (DV.Cantidad * DV.Precio) AS Subtotal, V.Total 
    FROM (((Facturas AS F
    INNER JOIN DetalleVenta AS DV ON F.ID_DetalleVenta = DV.ID_Detalle)
    INNER JOIN Ventas AS V ON DV.ID_Venta = V.ID_Venta)
    INNER JOIN Clientes AS C ON V.ID_Cliente = C.ID_Cliente)
    INNER JOIN Productos AS P ON DV.ID_Producto = P.ID_Producto
    WHERE F.NumeroFactura = ?
""", (numero_factura,))

factura = cursor.fetchall()

if not factura:
    print("Error: No se encontró la factura con el número:", numero_factura)
    sys.exit(1)

# Crear carpeta en C:\ si no existe
carpeta_facturas = r"C:\FacturasPDF"
if not os.path.exists(carpeta_facturas):
    os.makedirs(carpeta_facturas)

# Ruta donde se guardará el PDF
pdf_path = os.path.join(carpeta_facturas, f"{numero_factura}.pdf")

# Crear el PDF
c = canvas.Canvas(pdf_path, pagesize=letter)

c.drawString(100, 750, f"Factura: {numero_factura}")
c.drawString(100, 730, f"Fecha: {factura[0][1]}")
c.drawString(100, 710, f"Cliente: {factura[0][2]}")
c.drawString(100, 690, f"Cédula: {factura[0][3]} - RIF: {factura[0][4]}")

y = 650
for row in factura:
    c.drawString(100, y, f"Producto: {row[5]} | Cantidad: {row[6]} | Precio: {row[7]} | Subtotal: {row[8]}")
    y -= 20

c.drawString(100, y - 40, f"Total: {factura[0][9]}")
c.save()

print("Factura generada correctamente:", pdf_path)
