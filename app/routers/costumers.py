from fastapi import APIRouter, HTTPException, status

from models import Customer, CustomerUpdate, CustomerCreate
from db import SessionDep
from sqlmodel import select

router = APIRouter(tags=['Customers'])

@router.get('/costumers', response_model=list[Customer])  # response_model es para especificar que tipo de respuesta va a devolver en este caso una lista de objetos de tipo Customer
async def list_costumers(session: SessionDep):
    return session.exec(select(
        Customer)).all()  # select requiere un parametro que debe ser una entidad, en este caso le pasamos la entidad Customer y el .all significa que nos traiga todos los registros


@router.get('/costumers/{id}',  response_model=Customer)
async def get_customer(id: int,
                       session: SessionDep):  # recordar que cuando colocamos parentesiss en nuestro metodo del servicio, significa que estamos esperando un parametro o un body como en los casos anteriores
    try:
        customer = session.get(Customer,
                               id)  # en este caso estamos buscando un cliente por su id, si no lo encuentra nos va a devolver un error
        if customer is None:  # en este caso estamos validando si el cliente no existe, especificamos que error enviar
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:  # en este caso estamos capturando cualquier error que pueda ocurrir
        raise HTTPException(status_code=500, detail=str(e))
    return customer


@router.post('/createCostumer',
          response_model=Customer)  # response_model es para especificar que tipo de respuesta va a devolver en este caso un objeto de tipo Customer para devolver el id
async def create_costumer(costumer_data: CustomerCreate, session: SessionDep):
    # definimos una variable para guardar los datos despues de la validacion
    customer = Customer.model_validate(costumer_data.model_dump())  # esto nos devuelve todos los datos que esta ingresando el usuario como un diccionario
    # model_validate es un metodo para validar los datos que vienen del usuario, en este caso los datos que vienen del usuario los convertimos en un diccionario con model_dump y luego convierte esos datos a un objeto de tipo Customer
    # los datos que vienen del usuario los convertimos en un diccionario con model_dump y luego convierte esos datos a un objeto de tipo Customer
    session.add(customer)  # agregamos el objeto a la sesion
    session.commit()  # guardamos los datos en la base de datos, en el caso de sqlmodel cuando queremos ejecutar acciones, siempre debemos colocar esta variable commit, significa que esta generando la sentencia sql y la ejecuta en nuestro motor de base de datos
    session.refresh(customer)  # en este caso estamos refrescando la variable customer en memoria
    return customer


@router.delete('/costumers/{id}')
async def delete_customer(id: int, session: SessionDep):  # recordar que cuando colocamos parentesiss en nuestro metodo del servicio, significa que estamos esperando un parametro o un body como en los casos anteriores
    try:
        customer = session.get(Customer,id)  # en este caso estamos buscando un cliente por su id, si no lo encuentra nos va a devolver un error
        if customer is None:  # en este caso estamos validando si el cliente no existe, especificamos que error enviar
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:  # en este caso estamos capturando cualquier error que pueda ocurrir
        raise HTTPException(status_code=500, detail=str(e))

    session.delete(customer)
    session.commit()  # para hacer un cambio a la base de datos, sea eliminar, insertar, o actualizar debemos confirmarla con commit() solo para el caso de sqlmodel
    return {"detail:" "Customer deleted"}


@router.patch('/costumers/{id}',  response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):  # recordar que cuando colocamos parentesiss en nuestro metodo del servicio, significa que estamos esperando un parametro o un body como en los casos anteriores
    try:
        customer = session.get(Customer,
                               id)  # en este caso estamos buscando un cliente por su id, si no lo encuentra nos va a devolver un error
        if customer is None:  # en este caso estamos validando si el cliente no existe, especificamos que error enviar
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:  # en este caso estamos capturando cualquier error que pueda ocurrir
        raise HTTPException(status_code=500, detail=str(e))

    customer_data_dict = customer_data.model_dump(
        exclude_unset=True)  # esto nos devuelve todos los datos que esta ingresando el usuario como un diccionario y exclude_unset=True significa que no vamos a actualizar los campos que no se estan enviando
    customer.sqlmodel_update(customer_data_dict)  # en este caso estamos actualizando los datos del cliente
    session.add(customer)  # agregamos el objeto a la sesion
    session.commit()  # para hacer un cambio a la base de datos, sea eliminar, insertar, o actualizar debemos confirmarla con commit() solo para el caso de sqlmodel
    session.refresh(customer)  # en este caso estamos refrescando la variable customer en memoria
    return customer
