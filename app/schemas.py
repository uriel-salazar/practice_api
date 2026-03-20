from pydantic import BaseModel,Field


class Create_User(BaseModel):
    """ A Pydantic model that check users email, age
    and validate if their name is above 15.

    Args:
        BaseModel (class): A base class for creating pydantic models. 
    """
    name : str 
    age : int = Field(..., gt=15)
    email : str 
    
    
class User_Response(BaseModel):
    id : int
    name : str
    email : str
    