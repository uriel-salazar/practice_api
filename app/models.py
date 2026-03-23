from .database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey

class User(Base):
    """ A table that inherits from the declarative Base
    it prepares a metaobject to  be mapped to a sql table.

    Args:
        Base (_type_): Declarative Base
    """
    __tablename__='user'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)
    age:Mapped[int] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False,unique=True)
    posts:Mapped[list["Post"]] =relationship("Post",back_populates='user')


class Post(Base):
    """ A table called "post" that it will have a relationship with 
    user.id from the user's table. 

    Args:
        Base (_type_): _description_
    """
    __tablename__='post'
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=True)
    user:Mapped['User'] = relationship('User',back_populates='posts')



