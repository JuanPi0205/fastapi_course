# FastAPI Movies API

Welcome to the **Movies API**, a RESTful API built with **FastAPI**. This API allows you to perform CRUD operations (create, read, update, delete) on movie information, providing detailed data for each title.

## Features
- **Get movie information**: Retrieve detailed data such as title, genre, synopsis, and rating.
- **Add new movies**: Add new movies to the collection.
- **Update existing information**: Update the data of a specific movie.
- **Delete movies**: Remove a movie from the collection.
- **Filter movies by category**: Retrieve a list of movies based on their category.

## Technologies Used
- **FastAPI**: To quickly and efficiently build the API.
- **Uvicorn**: As the ASGI server to run the application.
- **Pydantic**: For data validation and defining models.

## Installation
Follow these steps to set up the project locally.

### Prerequisites
- **Python 3.7+**: Required to run FastAPI.
- **Pip**: To install dependencies.

### Installation Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/JuanPi0205/fastapi_movies.git
   ```
2. Navigate to the project directory:
   ```sh
   cd fastapi_movies
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Linux/MacOS:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
5. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
To start the development server, run the following command:
```sh
uvicorn main:app --reload --port 3000 --host 0.0.0.0
```
This will start the API at `http://localhost:3000/docs`.

You can access the interactive API documentation using **Swagger** at the following URL:
```
http://localhost:3000/docs
```
Or use the alternative **ReDoc** documentation at:
```
http://localhost:3000/redoc
```

## Endpoints
- **GET /**: Displays a welcome message in HTML.
- **GET /obtenerPeliculas**: Retrieves a list of all movies.
- **GET /obtenerPeliculas/{id}**: Retrieves the details of a specific movie.
- **GET /obtenerPeliculasCategoria/**: Retrieves a list of movies by category.
- **POST /createMovie**: Adds a new movie.
- **PUT /modificarMovie/{id}**: Updates movie information.
- **DELETE /eliminarMovie/{id}**: Deletes a movie.

## Contributions
Contributions are welcome. If you wish to contribute, please open a **pull request** or create an **issue** to discuss changes or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- **FastAPI**: For providing a powerful tool to build modern APIs.
- **Uvicorn**: For being a fast and efficient server for ASGI applications.

If you have any questions or want to contribute, feel free to open an issue. Enjoy exploring the world with this API!

