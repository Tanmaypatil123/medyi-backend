from typing import Dict

from api.models import CustomUser, UserAiCharacter


def get_or_create_user(*, email: str):
    return CustomUser.objects.get_or_create(email=email, is_deleted=False)


def create_user_ai_character(*, user_id: int, data: Dict):
    return UserAiCharacter.objects.create(user_id=user_id,properties=data)
