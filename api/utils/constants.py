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


FEMAL_AI_BOT_URL = [
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-asian.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-bangs.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-braids.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-bun.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-curly.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-ebony.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-euro.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-latina.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-middleeastern.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-nativeamerican.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-pigtails.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/female-southasian.webp",
    "https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/indian.webp",
]

MALE_AI_BOT_URL = [
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-ebony.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-euro.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-latina.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-middleeastern.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-mohawk.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-nativeamerican.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-sidepart.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-slickback.webp",
"https://d1jns1sy0m2jd7.cloudfront.net/frnd_media/post_media/male-southasian.webp",
]
