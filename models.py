from sqlalchemy import Column, Integer, String, Date, BigInteger, Numeric, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AsignacionEst(Base):
    __tablename__ = 'ASIGNACION_EST'
    __table_args__ = {'schema': 'public'}

    ID_ASIGNACION = Column(Integer, primary_key=True, autoincrement=True)
    ID_EST = Column(BigInteger, ForeignKey('public.ESTUDIANTES.ID_EST'), nullable=False)
    ID_SECCION = Column(BigInteger, ForeignKey('public.SECCIONES.ID_SECCION'), nullable=False)
    YEAR_ESCOLAR = Column(Date)
    FECHA_ASIGNACION = Column(Date)

    estudiante = relationship("Estudiantes", backref="asignaciones")
    seccion = relationship("Secciones", backref="asignaciones")

class AsistenciaEstudiantes(Base):
    __tablename__ = 'ASISTENCIA_ESTUDIANTES'
    __table_args__ = {'schema': 'public'}

    ID_ASISTENCIA_ESTUD = Column(Integer, primary_key=True, autoincrement=True)
    ID_EST = Column(BigInteger, ForeignKey('public.ESTUDIANTES.ID_EST'), nullable=False)
    ID_SECCION = Column(BigInteger, ForeignKey('public.SECCIONES.ID_SECCION'), nullable=False)
    FECHA_ASISTENCIA = Column(Date, nullable=False)
    ESTADO_ASISTENCIA = Column(Boolean, nullable=False, default=False)
    YEAR_ESCOLAR = Column(String(10), nullable=False)
    JUSTIFICACION = Column(Boolean)

    estudiante = relationship("Estudiantes", backref="asistencias_estudiantes")
    seccion = relationship("Secciones", backref="asistencias_estudiantes")

class AsistenciaProfesores(Base):
    __tablename__ = 'ASISTENCIA_PROFESORES'
    __table_args__ = {'schema': 'public'}

    ID_ASISTENCIA_PROF = Column(Integer, primary_key=True, autoincrement=True)
    ID_PROF = Column(BigInteger, ForeignKey('public.PROFESORES.ID_PROF'), nullable=False)
    FECHA_ASISTENCIA = Column(Date, nullable=False)
    ESTADO_ASISTENCIA = Column(Boolean, nullable=False)
    YEAR_ESCOLAR = Column(String(10), nullable=False)
    JUSTIFICACION = Column(Boolean)

    profesor = relationship("Profesores", backref="asistencias_profesores")

class Calificaciones(Base):
    __tablename__ = 'CALIFICACIONES'
    __table_args__ = {'schema': 'public'}

    ID_CALIFICACION = Column(Integer, primary_key=True, autoincrement=True)
    ID_EST = Column(BigInteger, ForeignKey('public.ESTUDIANTES.ID_EST'), nullable=False)
    ID_MATERIA = Column(BigInteger, ForeignKey('public.MATERIAS.ID_MATERIA'), nullable=False)
    CALIFICACION = Column(Numeric(10,0), nullable=False)
    ID_SECCION = Column(BigInteger, ForeignKey('public.SECCIONES.ID_SECCION'), nullable=False)
    YEAR_ESCOLAR = Column(Date, nullable=False)
    FECHA_CALIFICACION = Column(Date, nullable=False)

    estudiante = relationship("Estudiantes", backref="calificaciones")
    materia = relationship("Materias", backref="calificaciones")
    seccion = relationship("Secciones", backref="calificaciones")

class Estudiantes(Base):
    __tablename__ = 'ESTUDIANTES'
    __table_args__ = {'schema': 'public'}

    ID_EST = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_EST = Column(String(255))
    APELLIDO_EST = Column(String(255))
    CEDULA = Column(BigInteger, unique=True)
    CEDULA_EST = Column(BigInteger)
    FECHA_NAC = Column(Date)
    FECHA_REG = Column(Date)
    ESTADO = Column(String(50))
    DESCRIPCION_ESTADO = Column(String(255))
    GENERO = Column(String)
    CONDICION = Column(String(100))
    EMAIL_EST = Column(String(60))
    TELEFONO_EST = Column(BigInteger)

class Grados(Base):
    __tablename__ = 'GRADOS'
    __table_args__ = {'schema': 'public'}

    ID_GRADOS = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_GRADO = Column(String(255), nullable=False)
    FECHA_CREACION = Column(Date, nullable=False)

class Incidencias(Base):
    __tablename__ = 'INCIDENCIAS'
    __table_args__ = {'schema': 'public'}

    ID_INCIDENCIA = Column(Integer, primary_key=True, autoincrement=True)
    ID_EST = Column(Integer, ForeignKey('public.ESTUDIANTES.ID_EST'), nullable=False)
    ID_PROF = Column(Integer, ForeignKey('public.PROFESORES.ID_PROF'), nullable=False)
    FECHA = Column(Date, nullable=False)
    DESCRIPCION = Column(Text, nullable=False)
    CAUSA = Column(Text, nullable=False)

    estudiante = relationship("Estudiantes", backref="incidencias")
    profesor = relationship("Profesores", backref="incidencias")

class Materias(Base):
    __tablename__ = 'MATERIAS'
    __table_args__ = {'schema': 'public'}

    ID_MATERIA = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_MATERIA = Column(String(255), nullable=False)
    DESCRIPCION_MATERIA = Column(String(255), nullable=False)
    FECHA_CREACION = Column(Date, nullable=False)

class Profesores(Base):
    __tablename__ = 'PROFESORES'
    __table_args__ = {'schema': 'public'}

    ID_PROF = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_PROF = Column(String(255))
    APELLIDO_PROF = Column(String(255))
    CEDULA_PROF = Column(BigInteger, unique=True)
    TELEFONO_PROF = Column(BigInteger)
    DIRECCION_PROF = Column(String(255))
    FECHA_REG_PROF = Column(Date)
    EMAIL_PROF = Column(String(70))
    ID_ROL = Column(Integer, ForeignKey('public.ROLES.ID_ROL'))
    ID_ACCESO = Column(UUID(as_uuid=True), default='gen_random_uuid()') # PostgreSQL specific
    FECHA_NAC_PERSONAL = Column(Date)
    CODIFICACION = Column(String(10))
    CATEGORIA = Column(String(10))
    ESTUDIOS_ACTUAL = Column(String(10))
    FECHA_LABORAL = Column(Date)
    TURNO = Column(String(150))
    ESTADO = Column(String(30))

    rol = relationship("Roles", backref="profesores")

class Representantes(Base):
    __tablename__ = 'REPRESENTANTES'
    __table_args__ = {'schema': 'public'}

    ID_REP = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_REP = Column(String(255))
    APELLIDO_REP = Column(String(255))
    CEDULA_REP = Column(BigInteger, unique=True)
    TELEFONO_REP = Column(BigInteger)
    DIRECCION_REP = Column(String(255))
    FECHA_NAC_REP = Column(Date)
    FECHA_REG_REP = Column(Date)

class RepreEst(Base):
    __tablename__ = 'REPRE_EST'
    __table_args__ = {'schema': 'public'}

    ID_REPRE_EST = Column(Integer, primary_key=True, autoincrement=True)
    ID_REPRE = Column(BigInteger, ForeignKey('public.REPRESENTANTES.ID_REP'), nullable=False)
    ID_EST = Column(BigInteger, ForeignKey('public.ESTUDIANTES.ID_EST'), nullable=False)
    RAZON = Column(String(100))
    FECHA_CAMBIO = Column(Date)
    CAMBIO_DE = Column(String(150))
    ESTADO = Column(String(20))
    FECHA_REG = Column(Date)

    representante = relationship("Representantes", backref="repre_est")
    estudiante = relationship("Estudiantes", backref="repre_est")

class Roles(Base):
    __tablename__ = 'ROLES'
    __table_args__ = {'schema': 'public'}

    ID_ROL = Column(Integer, primary_key=True, autoincrement=True)
    ROL = Column(String(100), nullable=False, unique=True)

class Secciones(Base):
    __tablename__ = 'SECCIONES'
    __table_args__ = {'schema': 'public'}

    ID_SECCION = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_SECCION = Column(String(255))
    ID_GRADO = Column(BigInteger, ForeignKey('public.GRADOS.ID_GRADOS'), nullable=False)
    ID_PROF = Column(BigInteger, ForeignKey('public.PROFESORES.ID_PROF'), nullable=False)
    FECHA_CREA_ASIG = Column(Date, nullable=False)

    grado = relationship("Grados", backref="secciones")
    profesor = relationship("Profesores", backref="secciones")

class SeccionesMaterias(Base):
    __tablename__ = 'SECCIONES_MATERIAS'
    __table_args__ = {'schema': 'public'}

    ID_SECCION_MATERIA = Column(Integer, primary_key=True, autoincrement=True)
    ID_SECCION = Column(BigInteger, ForeignKey('public.SECCIONES.ID_SECCION'), nullable=False)
    ID_MATERIA = Column(BigInteger, ForeignKey('public.MATERIAS.ID_MATERIA'), nullable=False)
    FECHA_CREACION = Column(Date)

    seccion = relationship("Secciones", backref="secciones_materias")
    materia = relationship("Materias", backref="secciones_materias")

class TelefonosRepre(Base):
    __tablename__ = 'TELEFONOS_REPRE'
    __table_args__ = {'schema': 'public'}

    ID_TELEFONO = Column(Integer, primary_key=True, autoincrement=True)
    ID_REP = Column(BigInteger, ForeignKey('public.REPRESENTANTES.ID_REP'), nullable=False)
    TELEFONO = Column(BigInteger, nullable=False)
    TIPO_TELEFONO = Column(String(50))
    FECHA_REG = Column(Date, nullable=False, default='now()')

    representante = relationship("Representantes", backref="telefonos_repre")
