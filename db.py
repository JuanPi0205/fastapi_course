from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager


sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}" #aqui le estamos diciendo a sqlmodel que vamos a usar una base de datos sqlite y que el nombre de la base de datos es db.sqlite3

engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session: #with es una palabra clave que nos permite utilizar variables de otra clase internamente en la clase actual
        yield session #esto es programacion orientada asincrona, yield es muy parecido a un return pero con la diferencia de que podemos usarlo varias veces en una misma funcion
        #La primera vez que ejecutemos la función, la procesará hasta que encuentre el primer yield, la segunda vez, la función se ejecutará desde donde se quedó anteriormente, eso quiere decir que se ejecutará el código entre el primer yield y hasta el segundo y así sucesivamente hasta el último yield

SessionDep = Annotated[Session, Depends(get_session)] #Annotated es una clase que nos permite agregar metadatos a una variable, en este caso le estamos diciendo que la variable SessionDep es de tipo Session y que depende de la funcion get_session

@asynccontextmanager
async def lifespan(app):
        SQLModel.metadata.create_all(engine) #aqui le estamos diciendo a sqlmodel que cree todas las tablas que estan en la base de datos Y el parametro engine es la conexion a la base de datos
        print ("Database created succesfully")

        yield

        print("Closing application")