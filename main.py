import zoneinfo

from fastapi import FastAPI, Body, Path, Query, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import zoneinfo as tz
from models import Movie, Customer, Transaction, Invoice, CustomerCreate
from db import SessionDep

app = FastAPI()
app.title = 'Mi primera FastAPI'
app.version = '0.0.1'

movies = [
    {
        "id": 1,
        "titulo": "Batman",
        "resumen": "batman rompe todo",
        "año": "2017",
        "rating": 7.8,
        "categoria": "accion"
    },
    {
        "id": 2,
        "titulo": "Joker",
        "resumen": "Joker rompe a batman",
        "año": "2019",
        "rating": 6.8,
        "categoria": "accion"
    },
    {
        "id": 3,
        "titulo": "Ford vs Ferrari",
        "resumen": "Dos marcas un ganador",
        "año": "2020",
        "rating": 5.8,
        "categoria": "carreras"
    },
    {
        "id": 5,
        "titulo": "Ojo con la niña",
        "resumen": "Pilas con la niña que esta asustando",
        "año": "2020",
        "rating": 0.8,
        "categoria": "terror"
    }
]


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1> hola mundo</h1>')


@app.get('/obtenerPeliculas', tags=['movies'])
def get_movies():
    return JSONResponse(content=movies)

##colocamos response_model para especificar de que tipo va hacer la respuesta, en este caso como solo va a responder un objeto, diremos que es de tipo Movie
## o sea el array de objetos que tenemos arriba, tambien podemos especificar si queremos que devuelva una lista y de que tipo como vamos hacer abajo
@app.get('/obtenerPeliculas/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge= 1, le=1000)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    return JSONResponse(content=[], status_code=status.HTTP_404_NOT_FOUND)


@app.get('/obtenerPeliculasCategoria/', tags=['movies'], response_model=list[Movie])
##en este caso le especificamos que la respuesta va hacer un listado de peliculas de tipo Movie, porque pueden haber varias con la misma categoria
def get_movies_by_category(categoria: str = Query(min_length=4, max_length=16)) -> list[Movie]:
    data = [item for item in movies if item['categoria'] == categoria]
    return JSONResponse(content=data)


@app.post("/createMovie", tags=["movies"], response_model=dict)
def create_movie(movie: Movie) -> dict:
    ##tenemos que convertir nuestro array de objetos en un diccionario para que nos deje crear correctamente las peliculas nuevas
    if any(m['id'] == movie.id for m in movies):
        ##esta linea de if, es para validar si ya existe una pelicula con el id que viene, si es asi salta el httpException, con un status de codigo 400 y un mensaje
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")

    movie_dict = movie.model_dump()
    ##de esta manera convertirmos el objeto movie que es de tipo Movie, el cual es nuestro array de objetos en un diccionario
    movies.append(movie_dict)
    ##aqui agregamos lo que viene de nuestro servicio en el array de objetos
    return JSONResponse(content={"message": "Movie created"}, status_code= status.HTTP_201_CREATED)
    ##aqui le decimos que la respuesta sea un JSON, que contendra un objeto el cual tiene un mensaje que dice pelicula creada y un codigo de status 200

@app.put('/modificarMovie/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['titulo'] = movie.titulo
            item['resumen'] = movie.resumen
            item['año'] = movie.año
            item['rating'] = movie.rating
            item['categoria'] = movie.categoria
            return JSONResponse(content={"message":"Se ha modificado correctamente la pelicula"}, status_code=status.HTTP_200_OK)


@app.delete('/eliminarMovie/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se ha eliminado correctamente la pelicula seleccionada"}, status_code=status.HTTP_200_OK)


country_timezone = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "US": "America/New_York",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo"
}

@app.get('/horaServer', tags=['date'], response_model=dict)
def get_date():
    return JSONResponse(content={"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, status_code=status.HTTP_200_OK)

@app.get('/horaRecibir/{iso_code}', tags=['date'], response_model=dict)
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezone.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"date": datetime.now(tz)}

costumerArray = [{
    "id": 1,
    "name": "Juan Perez",
    "description": "Descripcion del cliente",
    "email": "test@mail.com",
    "age": 20
}]

db_customer: list[Customer] = [] #asumiendo que esta es nuestra base de datos
@app.post('/createCostumer',  tags=["Costumer"], response_model=Customer) #response_model es para especificar que tipo de respuesta va a devolver en este caso un objeto de tipo Customer para devolver el id
async def create_costumer(costumer_data: CustomerCreate, session:SessionDep):
    #definimos una variable para guardar los datos despues de la validacion
    customer = Customer.model_validate(costumer_data.model_dump()) #esto nos devuelve todos los datos que esta ingresando el usuario como un diccionario
    #model_validate es un metodo para validar los datos que vienen del usuario, en este caso los datos que vienen del usuario los convertimos en un diccionario con model_dump y luego convierte esos datos a un objeto de tipo Customer
    #los datos que vienen del usuario los convertimos en un diccionario con model_dump y luego convierte esos datos a un objeto de tipo Customer

    customer.id = len(db_customer) #contamos cuantos elementos hay en esta lista y le asignamos el valor a id
    db_customer.append(customer) #agregamos el valor del id a la lista de la base de datos
    return customer.dict()

@app.get('/costumers',  tags=["Costumer"], response_model=list[Customer])
async def list_costumers():
    return db_customer

@app.get('/costumers/{id}',  tags=["Costumer"], response_model=Customer)
def get_customer(id: int = Path(ge= 1, le=100)) -> db_customer: #recordar que cuando colocamos parentesiss en nuestro metodo del servicio, significa que estamos esperando un parametro o un body como en los casos anteriores
    #recorremos por medio de un for la supuesta base de datos que acabamos de crear buscando dentro de ella un id que coincida con el de la consulta
    for item in db_customer:
        if item.id == id:
            return JSONResponse(content=item.dict(), status_code=status.HTTP_200_OK) #si encuentra el id que coincida con el de la consulta, devuelve el objeto, para poder verlo como JSON debemos convertir el objeto a un diccionario, por ello el .dict(
    return JSONResponse(content=[], status_code=status.HTTP_404_NOT_FOUND)

@app.post('/transactions',  tags=["Costumer"], response_model=dict)
async def create_transaction(transaction_data: Transaction):
    if any(m['id'] == transaction_data.id for m in costumerArray):
        raise HTTPException(status_code=400, detail="Transaction with this ID already exists")

    movie_dict = transaction_data.model_dump()
    costumerArray.append(movie_dict)
    return JSONResponse(content={"message": "Transaction created"}, status_code=status.HTTP_201_CREATED)

@app.post('/invoices',  tags=["Costumer"], response_model=dict)
async def create_invoice(invoice_data: Invoice):
    if any(m['id'] == invoice_data.id for m in costumerArray):
        raise HTTPException(status_code=400, detail="Invoice with this ID already exists")

    movie_dict = invoice_data.model_dump()
    costumerArray.append(movie_dict)
    return JSONResponse(content={"message": "Invoice created"}, status_code=status.HTTP_201_CREATED)


