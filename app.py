from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "postgresql://user:password@localhost:5432/tu_base_de_datos"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de la base de datos
class Cliente(Base):
    __tablename__ = "clientes"
    cc = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    referencia_pago_id = Column(Integer, ForeignKey("referencias_pago.id"), nullable=False)

class ReferenciaPago(Base):
    __tablename__ = "referencias_pago"
    id = Column(Integer, primary_key=True, index=True)
    medio_pago = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    fecha_cancelacion = Column(Date, nullable=False)
    estado = Column(String, nullable=False)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Esquemas para la API
class ClienteBase(BaseModel):
    nombre: str
    cc: int
    telefono: str
    referencia_pago_id: int

class ReferenciaPagoBase(BaseModel):
    id: int
    medio_pago: str
    monto: float
    fecha_cancelacion: str
    estado: str

# Aplicación FastAPI
app = FastAPI()

@app.post("/clientes/")
def crear_cliente(cliente: ClienteBase):
    db = SessionLocal()
    nuevo_cliente = Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    db.close()
    return nuevo_cliente

@app.post("/referencias/")
def crear_referencia_pago(referencia: ReferenciaPagoBase):
    db = SessionLocal()
    nueva_referencia = ReferenciaPago(**referencia.dict())
    db.add(nueva_referencia)
    db.commit()
    db.refresh(nueva_referencia)
    db.close()
    return nueva_referencia

@app.get("/clientes/{cc}")
def obtener_cliente(cc: int):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.cc == cc).first()
    db.close()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@app.get("/referencias/{id}")
def obtener_referencia(id: int):
    db = SessionLocal()
    referencia = db.query(ReferenciaPago).filter(ReferenciaPago.id == id).first()
    db.close()
    if not referencia:
        raise HTTPException(status_code=404, detail="Referencia no encontrada")
    return referencia