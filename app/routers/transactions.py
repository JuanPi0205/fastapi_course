from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from db import SessionDep
from models import Transaction, TransactionCreate, Customer

router = APIRouter(tags=['Transactions'])

@router.post('/createTransactions')
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('costumer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")

    transaction_db = Transaction.model_validate(transaction_data_dict)

    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db
@router.get('/listTransactions')
async def list_transactions(session: SessionDep):
    query = select(Transaction)

    transactions = session.exec(query).all()
    return transactions
