from pydantic import BaseModel,Field,EmailStr,field_validator


class Create_User(BaseModel):
    """ A Pydantic model that check users email, age
    and validate if their name is above 15.

    Args:
        BaseModel (class): A base class for creating pydantic models. 
    """
    name : str =Field(...,min_length=3,max_length=20)
    age : int = Field(..., gt=15,le=120)
    email : EmailStr
       
    
class User_Response(BaseModel):
    id : int
    age:int
    name : str
    email : str
    
class Update_User(BaseModel):
    name:str = Field(...,min_length=3,max_length=20)
    age:int = Field(..., gt=15,le=120)
    email:EmailStr
    