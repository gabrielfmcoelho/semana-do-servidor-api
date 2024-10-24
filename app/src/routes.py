from fastapi import APIRouter, HTTPException, status, Response, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from .repository import PessoaRepository
from .settings import app_settings

# Define the header where the API key will be passed
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Function to verify the API key
def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key == app_settings.security_token:
        return api_key
    raise HTTPException(
        status_code=401,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "Bearer"},
    )

application_router = APIRouter(
    prefix="/api",
    tags=["sorteio"],
    dependencies=[Depends(verify_api_key)],
    responses={404: {"description": "Not found"}},
)

@application_router.get("/servidores")
async def get_government_employees():
    try:
        pessoas = PessoaRepository().get_pessoas()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not pessoas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum servidor disponível")
    return {"message": "Lista de servidores na base", "data": pessoas}

@application_router.get("/servidores/validados")
async def get_validated_government_employees():
    try:
        pessoas = PessoaRepository().get_validated_pessoas()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not pessoas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum servidor validado")
    return {"message": "Lista de servidores cadastrados pelo site", "data": pessoas}

@application_router.get("/servidores/{cpf}")
async def get_government_employee(cpf: str):
    try:
        pessoa = PessoaRepository().get_pessoa(cpf)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not pessoa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servidor não encontrado")
    return {"message": "Servidor encontrado", "data": pessoa}

@application_router.post("/servidores/{cpf}/validar")
async def validate_government_employee(cpf: str, force: bool = False, observation: str = 'terceirizado'):
    try:
        err, sts = PessoaRepository().validate_pessoa(cpf, force, observation)
        if not err:
            pessoa = PessoaRepository().get_pessoa(cpf)        
            return {"message": "Servidor validado com sucesso", "data": pessoa}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if err and sts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=sts)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servidor não encontrado")

@application_router.post("/sortear")
async def draw_government_employee():
    try:
        pessoa_cpf = PessoaRepository().draw_random_pessoa()
        if pessoa_cpf:
            pessoa = PessoaRepository().get_pessoa(pessoa_cpf)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not pessoa_cpf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum servidor disponível para sorteio")
    return {"message": "Servidor sorteado", "data": pessoa}

@application_router.get("/sorteados")
async def get_drawn_government_employees():
    try:
        pessoas = PessoaRepository().get_draw_pessoa()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    if not pessoas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum servidor sorteado")
    return {"message": "Lista de servidores sorteados", "data": pessoas}

@application_router.post("/limpar/validados")
async def clean_validated_government_employees():
    PessoaRepository().clean_validated()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@application_router.post("/limpar/sorteio")
async def clean_drawn_government_employees():
    PessoaRepository().clean_drawn()
    return Response(status_code=status.HTTP_204_NO_CONTENT)