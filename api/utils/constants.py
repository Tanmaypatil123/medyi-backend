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
    received_message = "received_message"



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
