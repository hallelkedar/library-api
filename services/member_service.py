from fastapi import HTTPException
from services.app_service import member_db

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