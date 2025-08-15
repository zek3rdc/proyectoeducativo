# 🏫 Sistema de Gestión Educativa con Streamlit
Este es un proyecto de aplicación web desarrollado con Streamlit, diseñado para ser un sistema integral de gestión para instituciones educativas. La plataforma permite administrar la información de estudiantes, profesores, calificaciones, asistencias y mucho más, todo desde una interfaz web interactiva y amigable.

## ✨ Características Principales
**🔐 Autenticación de Usuarios: Sistema de inicio de sesión seguro para distintos roles (ej. administradores).**

**👤 Gestión de Perfiles (CRUD):**

- Administración completa de Estudiantes.

- Administración de Profesores.

- Administración de Representantes.

**📚 Control Académico:**

- Registro y seguimiento de Calificaciones.

- Control de Asistencias para estudiantes y personal.

- Gestión de Grados, Secciones y Materias.

**📊 Dashboard Interactivo:**

- Visualización de datos clave sobre el rendimiento estudiantil.

- Gráficos estadísticos para un análisis rápido.

**📄 Importación y Exportación:**

- Capacidad para importar datos masivos desde archivos Excel/CSV.

- Generación de reportes y facturas en formato Excel.

## 🗃️ Base de Datos Robusta: Utiliza SQLAlchemy para el manejo de la base de datos y Alembic para las migraciones.


## 💻 Tecnologías Utilizadas
🛠️ Instalación y Puesta en Marcha
Sigue estos pasos para ejecutar el proyecto en tu máquina local.

**Prerrequisitos**
Tener instalado Python 3.8 o superior.

Tener pip (el gestor de paquetes de Python) actualizado.

Pasos de Instalación
Clonar el repositorio:

git clone https://github.com/tu-usuario/proyectoeducativo.git
cd proyectoeducativo

(Recomendado) Crear y activar un entorno virtual:

En Windows:

python -m venv venv
.\venv\Scripts\activate

En macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Instalar las dependencias:

pip install -r requirements.txt

Configurar los usuarios:

Abre el archivo config.yaml.

Dentro de credentials, puedes añadir o modificar los usuarios, nombres y contraseñas. Recuerda usar contraseñas seguras.

Inicializar la base de datos (si es necesario):
La aplicación utiliza SQLite, por lo que el archivo database.db se creará automáticamente. Las migraciones se manejan con Alembic.

alembic upgrade head

**▶️ Ejecutar la Aplicación**
Una vez completada la instalación, inicia el servidor de Streamlit con el siguiente comando:

streamlit run app.py

Abre tu navegador y ve a la dirección URL que aparece en la terminal (normalmente http://localhost:8501).

# 👤 Autor
Zek3rdc
