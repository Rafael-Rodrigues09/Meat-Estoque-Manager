import os
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from services import create_data, add_usage, add_rest, reset, get_data, reverse, get_history, add_lot, get_lot
from schemas import ModeloRegistro, ModeloLot
from datetime import date

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def api_door(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Acesso negado")

app = FastAPI()
create_data()

@app.exception_handler(ValueError)
def ValueError_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={'detail': str(exc)})

@app.api_route('/health', methods=['GET', 'HEAD'])
def check_health(): return JSONResponse(status_code=200)

@app.get('/estoque')
def rote_show_data(verify = Depends(api_door)):
    return get_data()

@app.get('/historico')
def rote_show_history(verify = Depends(api_door)):
    return get_history()

@app.get('/allestoque')
def rote_show_lot(verify = Depends(api_door)):
    return get_lot()

@app.post('/add-estoque')
def rote_add_lot(data: ModeloLot, verify = Depends(api_door)):
    return add_lot(name=data.name, value=data.value, expiration_date=data.expiration_date)

@app.post('/uso')
def rote_uso(data: ModeloRegistro, verify = Depends(api_door)):
    return add_usage(data.name, data.value)
    
@app.post('/sobra')
def rote_sobra(data: ModeloRegistro, verify = Depends(api_door)):
    return add_rest(name=data.name, value=data.value)
    
@app.post('/reset')
def rote_reset(verify = Depends(api_door)):
    file = reset()
    return FileResponse(path=file, filename=f'Backup{date.today()}.pdf', media_type='application/pdf')


@app.post('/reverse')
def reverse_value(verify = Depends(api_door)):
    return reverse()





