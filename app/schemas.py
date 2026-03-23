from pydantic import BaseModel,Field,EmailStr,field_validator



class Create_User(BaseModel):
    """ A Pydantic model that check users email, age
    and validate if their name is above 15.
    """
    name: str
    age: int = Field(..., gt=15)
    email: EmailStr

    @field_validator("email")
    def lowercase_email(cls, b):
        return b.strip().lower()
    
class User_Response(BaseModel):
    id : int
    age:int
    name : str
    email : str
    
class Update_User(BaseModel):
    name:str
    age:int = Field(..., gt=15)
    email:EmailStr
    
    
