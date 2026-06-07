from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

from repos.userrepo import UserRepository, get_user_repo
from schemas.userschema import UserRegistrate, UserResponse

class RegService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["sha512_crypt"])
                                        
    def hash_password(self, password):
        return self.pwd_context.hash(password)
    
    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.repo.get_by_email(email)
        return user

    async def create_user(self, data_dict: UserRegistrate) -> UserResponse:
        if await self.repo.get_by_email(data_dict.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user already exist")
        
        data_dump = data_dict.model_dump()
        data_dump["password"] = self.hash_password(data_dump["password"])

        user = await self.repo.create_user(data_dump)

        return user

async def get_reg_service(repo: UserRepository = Depends(get_user_repo)):
    return RegService(repo)