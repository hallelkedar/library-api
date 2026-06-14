from fastapi import APIRouter
from routes.model import Member, UpdateMember
from services.app_service import member_db
from services import member_service

router = APIRouter()

@router.get('')
def get_all_members():
    return member_db.get_all_members()

@router.post('')
def create_member(data: Member):
    member = data.model_dump()
    new_id = member_db.create_member(member)
    return {'detail': f'Member (-id-:{new_id}) created'}

@router.get('/{id}')
def get_member(id: int):
    return member_service.get_member(id)

@router.patch('/{id}')
def update_member(id, data: UpdateMember):
    member_data = data.model_dump(exclude_unset=True)
    member_service.get_member(id)
    member_db.update_member(id, member_data)
    return {'detail': f'Member (-id-:{id}) updated'}

@router.patch('/{id}/deactivate')
def deactivate_member(id: int):
    member_service.set_member_activity(id, False)
    return {'detail': f'Member (-id-:{id}) is no longer active'}

@router.patch('/{id}/activate')
def activate_member(id: int):
    member_service.set_member_activity(id, True)
    return {'detail': f'Member (-id-:{id}) is active again'}