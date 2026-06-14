from fastapi import HTTPException
from services.app_service import member_db
from logs.logger import logger


def get_all_members():
    all_members = member_db.get_all_members()
    if not all_members:
        logger.warning('Members list is empty.')
    return all_members

def create_member(data: dict):
    new_id = member_db.create_member(data)
    if not new_id:
        raise HTTPException(400, 'Email is used by another member')
    return new_id

def get_member(member_id: int) -> dict | None:
    member = member_db.get_member_by_id(member_id)
    if not member:
        raise HTTPException(404, 'Member not found.')
    
    return member

def set_member_activity(member_id: int, active: bool):
    member = get_member(member_id)
    if active:
        if member['is_active']:
            raise HTTPException(400, 'Member is already active')
        member_db.activate_member(member_id)
        return
    if not member['is_active']:
        raise HTTPException(400, 'Member is already deactive')
    member_db.deactivate_member(member_id)