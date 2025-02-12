import os
import base64
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Definir los alcances requeridos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Si modificas los alcances, elimina el archivo token.json
TOKEN_FILE = 'token.json'  # El archivo donde guardamos el token de acceso de OAuth

# Función para obtener el servicio de Gmail
def obtener_servicio_gmail():
    creds = None
    # El archivo token.json guarda el token de acceso y el refresco de OAuth.
    # Si no existe, se genera uno nuevo.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si no hay credenciales disponibles o son inválidas, solicita el acceso
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Este es el archivo credentials.json
            creds = flow.run_local_server(port=0)
        
        # Guarda las credenciales para la próxima ejecución
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Usar las credenciales para construir el servicio de Gmail
    return build('gmail', 'v1', credentials=creds)

# Función para enviar un correo usando la API de Gmail
def enviar_correo_nuevo_profesor(nombre, apellido, cedula, email, rol):
    try:
        # Configurar el mensaje
        asunto = "🎉 ¡Has sido contratado en UENB!"
        cuerpo = f"""
        Estimado/a {nombre} {apellido},

        Nos complace informarte que has sido contratado en nuestra institución.

        📌 **Detalles de tu contratación:**
        - **Cédula:** {cedula}
        - **Cargo:** {rol}

        Bienvenido/a al equipo de UENB. Nos pondremos en contacto contigo pronto.

        Saludos,
        Equipo UENB
        """

        # Crear el mensaje de correo
        mensaje = MIMEMultipart()
        mensaje['From'] ="asuntosuts@gmail.com"  # Tu correo de Gmail
        mensaje['To'] = email
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Codificar el mensaje en base64
        raw_message = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

        # Obtener el servicio de Gmail
        servicio_gmail = obtener_servicio_gmail()

        # Enviar el correo usando la API de Gmail
        message = servicio_gmail.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Correo enviado: {message['id']}")
        return True  # ✅ Envío exitoso

    except HttpError as error:
        print(f"Un error ocurrió: {error}")
        return False  # ❌ Error en el envío
