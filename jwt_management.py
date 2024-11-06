from jwt import encode, decode
import os
from dotenv import load_dotenv


load_dotenv()

secretKey = os.getenv("SECRET_KEY")

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=secretKey, algorithm="HS256")
    return token