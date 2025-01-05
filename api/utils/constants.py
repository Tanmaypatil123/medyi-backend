from enum import Enum

AUTHENTICATION_HEADER = "HTTP_AUTHORIZATION"
APPVERSION_HEADER = "HTTP_APPVERSION"

AUTH_ERROR = "Invalid Request"

IMAGE_QUALITY_PARAMS = {
    'sharpness': 10,
    'brightness': 200,
    'contrast': 30,
    'saturation': 150,
    'noise_level': 10,
    'entropy': 5
}


IMAGE_QUALITY_WEIGHTS = {
    'sharpness': 2,
    'brightness': 2,
    'contrast': 1,
    'saturation': 2,
    'noise_level': 2,
    'entropy': 2
}


class ChatEvents(Enum):
    send_message_error = "send_message_error"
    on_read_receipt = "on_read_receipt"
    send_read_receipt = "send_read_receipt"
    new_message = "new_message"
    new_room = "new_room"
    updated_profile = 'updated_profile'
    profile_update_failed = "profile_update_failed"
    askout_received = "askout_received"
    update_chatlist = "update_chatlist"
    chatlist_on_read_receipt = "chatlist_on_read_receipt"
    updated_profile_images = "updated_profile_images"
