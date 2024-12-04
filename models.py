from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
class Costumer(BaseModel):
    id: Optional[int]
    name: str = Field(min_length=2, max_length=20)
    description: str | None = Field(min_length=2, max_length=400) #de esta manera con el None le decimos que puede ser nulo o sea que no es obligatorio
    email: EmailStr = Field(min_length=5, max_length=50) #de esta manera le decimos que el email tiene que tener un formato de email
    age: int = Field(ge=18, le=100) #de esta manera le decimos que la edad tiene que ser mayor o igual a 18 y menor o igual a 100

    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                "id": 1,
                "name": "Juan Perez",
                "description": "Descripcion del cliente",
                "email": "mail@mail.com",
                "age": 20
            }
        ]
    })

class Movie(BaseModel):
    id: Optional[int]
    titulo: str = Field(min_length=8,max_length=15)
    resumen: str = Field(min_length=10, max_length=400)
    año: str = Field(min_length=4, max_length=4)
    rating: float = Field( ge=1,le=10.0)
    categoria: str = Field(min_length=4, max_length=16)

    model_config = ConfigDict(json_schema_extra={
        'examples': [
            {
                "id": 1,
                "titulo": "Mi pelicula",
                "resumen": "Descripcion de la pelicula",
                "año": "2022",
                "rating": 9.8,
                "categoria": "Acción"
            }
        ]
    })

class Transaction(BaseModel):
    id: int
    ammonut: int | float
    description: str

class Invoice(BaseModel):
    id: int
    customer: Costumer
    transactions: list[Transaction]
    date: str
    total: int
    @property
    def ammount_total(self):
        return sum([t.ammonut for t in self.transactions])
