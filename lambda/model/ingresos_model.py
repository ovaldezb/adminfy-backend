from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

# Wrapper para que Pydantic v2 acepte ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _):
        from pydantic_core import core_schema
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

# Base model con types arbitrarios permitidos
class CustomBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

# Modelo detalle de ingreso
class DetalleIngreso(CustomBaseModel):
    categoria: str
    monto: float

# Modelo base de ingreso
class IngresoBase(CustomBaseModel):
    fecha: datetime
    monto_total: float
    descripcion: Optional[str] = None
    unidad_id: PyObjectId
    residente_id: PyObjectId
    metodo_pago: Optional[str] = None
    referencia: Optional[str] = None
    cuenta_origen: Optional[str] = None
    nombre_pagador: Optional[str] = None
    comprobante_url: Optional[str] = None
    detalle: List[DetalleIngreso]

# Crear ingreso
class IngresoCreate(BaseModel):
    
    fecha: datetime
    monto_total: float
    descripcion: Optional[str] = None
    unidad_id: str  # ← solo string, como "PIOMBINO-22"
    residente_id: str  # ← string como "JUAN PÉREZ"
    metodo_pago: Optional[str] = None
    referencia: Optional[str] = None
    cuenta_origen: Optional[str] = None
    nombre_pagador: Optional[str] = None
    comprobante_url: Optional[str] = None
    detalle: List[DetalleIngreso]


# Actualizar ingreso
class IngresoUpdate(CustomBaseModel):

    fecha: Optional[datetime] = None
    monto_total: Optional[float] = None
    descripcion: Optional[str] = None
    unidad_id: Optional[PyObjectId] = None
    residente_id: Optional[PyObjectId] = None
    metodo_pago: Optional[str] = None
    referencia: Optional[str] = None
    cuenta_origen: Optional[str] = None
    nombre_pagador: Optional[str] = None
    comprobante_url: Optional[str] = None
    detalle: Optional[List[DetalleIngreso]] = None

# Modelo completo con _id
class IngresoDB(IngresoBase):
    id: PyObjectId = Field(alias="_id")
    creado_en: datetime
    actualizado_en: datetime
