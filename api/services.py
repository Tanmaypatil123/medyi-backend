from typing import Dict

from api.selectors import get_or_create_user, create_user_ai_character
from api.tasks import create_ai_model_for_user_and_assign


def login_or_register_user(*,email:str)->Dict:
    user, created = get_or_create_user(email=email)
    data = {
        "is_new_user": created,
        "auth_token": "token",
        "access_token":"token"
    }
    # generated token for authication
    return data


def get_data_and_create_user_chat_model(*,data:Dict,user_id:int)->Dict:

    ai_character = create_user_ai_character(user_id=user_id, data=data)
    create_ai_model_for_user_and_assign.delay(user_id=user_id,ai_character_id=ai_character.id)



