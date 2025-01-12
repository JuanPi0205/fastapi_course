from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field #si un campo no tiene la variable Field entonces no se va a guardar en la base de datos

#en esta caso heredamos la clase principal desde sqlmodel para que se cree la tabla en la base de datos
class CostumerBase(SQLModel): #en este caso creamos un modelo base que se va a usar para crear un nuevo cliente y que se va a guardar en la base de datos
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)



class CustomerCreate(CostumerBase): #en este caso creamos un modelo aparte que no se va a guardar en la base de datos y que se va a usar para crear un nuevo cliente
    pass #El pass indica que no se necesita ninguna implementación adicional en esta clase, pero la clase no puede estar vacía, por lo que se usa pass para cumplir con la sintaxis de Python

class CustomerUpdate(CostumerBase):
    pass


#heredamos de CostumerBase para que se cree la tabla en la base de datos
class Customer(CostumerBase, table=True): #En este caso creamos un modelo aparte que si se va a guardar en la base de datos
    id: int | None = Field(default=None, primary_key=True) #colocamos un valor por defecto como None para cuando creemos el dato y no se lo estamos enviando, automaticamente se le asigne un valor


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
    customer: Customer
    transactions: list[Transaction]
    date: str
    total: int
    @property
    def ammount_total(self):
        return sum([t.ammonut for t in self.transactions])
