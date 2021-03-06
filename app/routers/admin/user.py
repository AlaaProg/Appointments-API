from fastapi import Body, APIRouter
from core.resource import resource, BaseResource
from app.schemas.user import AdminUser, AdminUpdateUser, CustomerProfileReadOnly, EmployeeProfileReadOnly
from app.repositories.user_repository import UserRepository


router = APIRouter(prefix="/user")

@resource(router)
class UserResource(BaseResource):

    repository = UserRepository()

    def index(self, role: int=None):

        return self.repository.all(role)

    def store(self, user: AdminUser):
        new_user = self.repository.create(**user.dict())

        return self.response(
            msg="Succesfuly delete", 
            data=new_user.parse())

    def show(self, id):
        obj = self.repository.get_or_failed(self.repository.model, id)
        
        if obj.customer: 
            return obj.parse(CustomerProfileReadOnly)
        
        if obj.employee:
  
            return obj.parse(EmployeeProfileReadOnly)

        return obj.parse()

    def delete(self, id):
        self.repository.delete()

        return self.response(
            msg="Succesfuly delete", 
            data={"id": id})

    def update(self, id: int, user: AdminUpdateUser):
        """Active Account"""    

        user = self.repository.update(id, **user.dict(exclude_unset=True))

        return self.response(
            msg="Succesfuly update ", 
            data=user.parse())
