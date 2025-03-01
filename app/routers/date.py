import zoneinfo

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter(tags=['DatesExamples'])

country_timezone = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "US": "America/New_York",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo"
}

@router.get('/horaServer', tags=['date'], response_model=dict)
def get_date():
    return JSONResponse(content={"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, status_code=status.HTTP_200_OK)

@router.get('/horaRecibir/{iso_code}', tags=['date'], response_model=dict)
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezone.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"date": datetime.now(tz)}
