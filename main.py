import zoneinfo

from fastapi import FastAPI, Body, Path, Query, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
import zoneinfo as tz

app = FastAPI()
app.title = 'Mi primera FastAPI'
app.version = '0.0.1'


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

