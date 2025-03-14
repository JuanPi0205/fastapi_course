from fastapi import Path, Query, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from models import Movie

router = APIRouter(tags=['Movies'])

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


@router.get('/obtenerPeliculas', )
def get_movies():
    return JSONResponse(content=movies)

##colocamos response_model para especificar de que tipo va hacer la respuesta, en este caso como solo va a responder un objeto, diremos que es de tipo Movie
## o sea el array de objetos que tenemos arriba, tambien podemos especificar si queremos que devuelva una lista y de que tipo como vamos hacer abajo
@router.get('/obtenerPeliculas/{id}', response_model=Movie)
def get_movie(id: int = Path(ge= 1, le=1000)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item, status_code=status.HTTP_200_OK)
    return JSONResponse(content=[], status_code=status.HTTP_404_NOT_FOUND)


@router.get('/obtenerPeliculasCategoria/', response_model=list[Movie])
##en este caso le especificamos que la respuesta va hacer un listado de peliculas de tipo Movie, porque pueden haber varias con la misma categoria
def get_movies_by_category(categoria: str = Query(min_length=4, max_length=16)) -> list[Movie]:
    data = [item for item in movies if item['categoria'] == categoria]
    return JSONResponse(content=data)


@router.post("/createMovie", response_model=dict)
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

@router.put('/modificarMovie/{id}', response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['titulo'] = movie.titulo
            item['resumen'] = movie.resumen
            item['año'] = movie.año
            item['rating'] = movie.rating
            item['categoria'] = movie.categoria
            return JSONResponse(content={"message":"Se ha modificado correctamente la pelicula"}, status_code=status.HTTP_200_OK)


@router.delete('/eliminarMovie/{id}', response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se ha eliminado correctamente la pelicula seleccionada"}, status_code=status.HTTP_200_OK)
