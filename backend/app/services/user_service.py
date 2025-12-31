from sqlalchemy.orm import Session
from app.schemas.users import UserCreate
from app.crud.user_crud import createUser, updateUser, change_user_password
from app.schemas.users import UserUpdate

def create_user_service(user: UserCreate, session: Session):
    with session.begin():
        db_user = createUser(user, session)
    return db_user

def update_user_service(user_id: int, data: UserUpdate, session: Session):
    updated_user = updateUser(user_id, data, session)
    session.commit()
    return updated_user

def change_user_password_service(user_id: int, current_password: str, new_password: str, session: Session):
    updated_user = change_user_password(user_id, current_password, new_password, session)
    session.commit()
    return updated_user
