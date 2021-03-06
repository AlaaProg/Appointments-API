from sqlalchemy import exc, Column, func, ForeignKey
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql import sqltypes as types
from sqlalchemy.orm import relationship, backref
from fastapi import HTTPException
from core.database import SessionLocal, engine, schema

class CustomProperty(property):
    """Custom Property To call func"""

    def __get__(self, _, cls):
        return self.fget(cls)

# Base Model
class BaseModel(schema.BaseSchema):
    """Base Model for  SqlAlchemy Model"""

    session:object = SessionLocal()

    __schema__ = None

    id:Column = Column(types.Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """Set a class name for the table """
        return cls.__name__.lower()

    @CustomProperty  
    def query(cls) -> object:
        """Get session query """
        return cls.session.query(cls)

    @classmethod 
    def create(cls, **kw:dict) -> list:
        """Create new raw"""
        try: 
            obj = cls(**kw)
            cls.session.add(obj)
            cls.session.commit()
            return obj 
        except exc.SQLAlchemyError as err:
            cls.session.rollback()
            raise HTTPException(403, detail={
                'ok': False,
                'errors': err.args
            })

    def _set(self, relate: str, model: object):
        self.__setattr__(relate, model)
        self.save()

    def _append(self, relate: str, model: object):
        relate_obj = self.__getattribute__(relate)
        relate_obj.append(model)
        self.save()

    @classmethod
    def get(cls, id) -> object:
        obj = cls.query.get(id)
        return obj
    
    @classmethod
    def update(cls, id, **kw:dict) -> list:
        try:
            obj = cls.query.filter_by(id=id)
            obj.update(kw)
            cls.session.commit()
            return obj.first()
        except exc.SQLAlchemyError as err:
            raise HTTPException(status_code=403, detail={
                'ok': False,
                'errors': err.args
            })  

    def save(self, **kw) -> list:
        """Commit object"""
        try: 
            if kw:
                self.query.filter_by(id=self.id).update(kw)
            else:
                self.session.add(self)
            self.session.commit()
            return 1
        except exc.SQLAlchemyError as err:
            self.session.rollback()
            raise HTTPException(status_code=403, detail={
                'ok': False,
                'errors': err.args
            })

    @classmethod
    def commit(cls):
        """Commit object"""
        try: 
            cls.session.commit()
            return 1
        except exc.SQLAlchemyError as err:
            cls.session.rollback()
            raise HTTPException(status_code=403, detail={
                'ok': False,
                'errors': err.args
            })

    # def update(self, **kw:dict) -> list:
    #     try:
    #         obj = self.query.filter_by(id=self.id)
    #         obj.update(kw)
    #         self.session.commit()
    #         return obj.first()
    #     except exc.SQLAlchemyError as err:
    #         raise HTTPException(status_code=403, detail={
    #             'ok': False,
    #             'errors': err.args
    #         })

    def delete(self):
        try: 
            self.session.delete(self)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as err:
            self.session.rollback()
            raise HTTPException(status_code=403, detail={
                'ok': False,
                'errors': err.args
            })

    def __repr__(self) -> str:

        return f"<{self.__class__.__name__}(id={self.id})>"
    

class TimeStamp(object):
    """Timestamp fields"""
    
    created_at = Column(types.TIMESTAMP, server_default=func.now())
    updated_at = Column(types.TIMESTAMP, server_default=func.now() , server_onupdate=func.now())

Model = declarative_base(cls=BaseModel)

def migrate():
    
    Model.metadata.create_all(bind=engine)

def drop():

    Model.metadata.drop_all(bind=engine)