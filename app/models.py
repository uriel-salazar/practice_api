from .database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,String

class User(Base):
    """ A table that inherits from the declarative Base
    it prepares a metaobject to  be mapped to a sql table.

    Args:
        Base (class) : Class inherited from Declarative Base
    """
    __tablename__='user' # name of the table
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age:Mapped[int] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(String(254),nullable=False,unique=True)
    
    posts:Mapped[list["Post"]] = relationship("Post",back_populates='user')


class Post(Base):
    """ A table called "post" that it will have a relationship with 
    user.id from the user's table. 

    Args:
        Base (_type_): _description_
    """
    __tablename__='post' # name of sql table. 
    
    id:Mapped[int] = mapped_column(primary_key=True)
    #foreign key
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    description:Mapped[str] = mapped_column(nullable=True)
    
    user:Mapped['User'] = relationship('User',back_populates='posts')



