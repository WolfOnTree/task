from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException, Query, UploadFile, File

from service.autchservice import get_auth_service, AuthService, get_auth_service_without_token
from service.regservice import get_reg_service, RegService
from schemas.userschema import UserRegistrate, UserResponse
from schemas.autchschema import Token, Login
from configs.settings import settings

router = APIRouter()

@router.post("/reg", response_model=UserResponse)    
async def reg( 
    data: UserRegistrate, service: RegService = Depends(get_reg_service)
):
    res = await service.create_user(data)

    return res

@router.post("/crt_tkn", response_model=Token)
async def create_token(
    form_data: Login,
    service: AuthService = Depends(get_auth_service_without_token)
):
    user = await service.autenticate_user(form_data.email, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    accses_token_exp = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = service.create_accsess_token(
        {"sub": user.email,}, accses_token_exp
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protect(service: AuthService = Depends(get_auth_service)):
    
    current_user = await service.get_curent_user()


    return {"access": "ok"} 