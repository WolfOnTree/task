from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from configs.settings import settings
from repos.userrepo import UserRepository, get_user_repo
from model.subjects import User

security = HTTPBearer()

class AuthService:
    def __init__(self, repo: UserRepository, credentials: HTTPAuthorizationCredentials | None = None):
        self.repo = repo
        self.credentials = credentials
        self.pwd_contex = CryptContext(schemes=["sha512_crypt"])

    def verefy_password(self, password:str, hash_password:str):
        return self.pwd_contex.verify(password, hash_password)
    
    async def autenticate_user(self, email: str, password) -> User:
        user = await self.repo.get_by_email(email)

        if not user:
            return False
        if not self.verefy_password(password, user.password):
            return False

        return user
    
    def create_accsess_token(self, data: dict, exp_time: timedelta = None) -> str:
        if exp_time:
            expire = datetime.utcnow() + exp_time
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        data.update({"exp": expire})

        encodet_jwt = jwt.encode(
            data,
            key=settings.secret_key,
            algorithm=settings.algorithm
        )

        return encodet_jwt
    
    async def get_curent_user(self) -> User:

        auth_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nor valid email or passwor",
        )

        try:
            payload = jwt.decode(
                self.credentials.credentials,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )

            email = payload.get("sub")

            if not email:
                raise auth_exeption
            
        except JWTError:
            raise auth_exeption

        user = await self.repo.get_by_email(email)

        if not user:
            raise auth_exeption

        return user


async def get_auth_service(
        repo: UserRepository = Depends(get_user_repo),
        credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthService:
    return AuthService(repo, credentials)


async def get_auth_service_without_token(
        repo: UserRepository = Depends(get_user_repo)):
    return AuthService(repo)