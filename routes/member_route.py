from fastapi import APIRouter
from routes.model import Member, UpdateMember, MemberResponse
from services.app_service import member_db
from services import member_service
from logs.logger import logger

router = APIRouter()

@router.get('', response_model=list[MemberResponse])
def get_all_members():
    all_members = member_service.get_all_members()
    logger.info('Return all members list')
    return all_members

@router.post('', status_code=201)
def create_member(data: Member):
    member = data.model_dump()
    new_id = member_service.create_member(member)

    return_msg = {'detail': f'Member (-id-:{new_id}) created'}
    logger.info(return_msg['detail'])
    return return_msg

@router.get('/{id}', response_model=MemberResponse)
def get_member(id: int):
    member = member_service.get_member(id)
    logger.info(f'Return member number - {id}')
    return member

@router.patch('/{id}')
def update_member(id, data: UpdateMember):
    member_data = data.model_dump(exclude_unset=True)
    member_service.get_member(id)
    member_db.update_member(id, member_data)
    
    return_msg = {'detail': f'Member (-id-:{id}) updated'}
    logger.info(return_msg['detail'])
    return return_msg

@router.patch('/{id}/deactivate')
def deactivate_member(id: int):
    member_service.set_member_activity(id, False)
    return_msg = {'detail': f'Member (-id-:{id}) is no longer active'}
    logger.info(return_msg['detail'])
    return return_msg

@router.patch('/{id}/activate')
def activate_member(id: int):
    member_service.set_member_activity(id, True)
    return_msg = {'detail': f'Member (-id-:{id}) is active again'}
    logger.info(return_msg['detail'])
    return return_msg