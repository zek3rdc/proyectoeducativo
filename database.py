from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base # Importa la Base de tus modelos

# Configura la URL de la base de datos desde alembic.ini o directamente
DATABASE_URL = "postgresql://zek3rdc:prueba12P$A@localhost:5432/BASE_EUNB"

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para crear todas las tablas (solo si no existen, útil para desarrollo inicial)
def create_all_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    # Ejemplo de uso:
    # Para crear las tablas si no existen (solo para desarrollo, las migraciones se encargan en producción)
    # create_all_tables()
    
    # Ejemplo de cómo obtener una sesión y usar un modelo
    from models import Estudiantes # Importa el modelo que quieras usar

    db = SessionLocal()
    try:
        # Consulta todos los estudiantes
        estudiantes = db.query(Estudiantes).all()
        print("Estudiantes en la base de datos:")
        for estudiante in estudiantes:
            print(f"ID: {estudiante.ID_EST}, Nombre: {estudiante.NOMBRE_EST}, Apellido: {estudiante.APELLIDO_EST}")
    except Exception as e:
        print(f"Error al consultar estudiantes: {e}")
    finally:
        db.close()
