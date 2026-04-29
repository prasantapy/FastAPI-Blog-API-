from pydantic import BaseModel, EmailStr

# 👉 Register
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 👉 Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 👉 Response (IMPORTANT)
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# 👉 Post schemas
class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True