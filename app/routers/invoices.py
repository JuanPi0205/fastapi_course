from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models import Invoice

router = APIRouter(tags=['Invoices'])

costumerArray = [{
    "id": 1,
    "name": "Juan Perez",
    "description": "Descripcion del cliente",
    "email": "test@mail.com",
    "age": 20
}]

@router.post('/invoices', response_model=dict)
async def create_invoice(invoice_data: Invoice):
    if any(m['id'] == invoice_data.id for m in costumerArray):
        raise HTTPException(status_code=400, detail="Invoice with this ID already exists")

    movie_dict = invoice_data.model_dump()
    costumerArray.append(movie_dict)
    return JSONResponse(content={"message": "Invoice created"}, status_code=status.HTTP_201_CREATED)


