from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from db import lifespan
from .routers import costumers, invoices, date, movies, transactions

app = FastAPI(title="Campamento FASTAPI", lifespan=lifespan)
app.include_router(costumers.router)
app.include_router(invoices.router)
app.include_router(date.router)
app.include_router(movies.router)
app.include_router(transactions.router)

@app.get('/', tags=['Home'])
def homePage():
    html_path = Path("app/templates/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)
