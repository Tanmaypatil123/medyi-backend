from django.contrib import admin
from api.Llmserver.models import LLMServers
from api.models import UserAiCharacter, AICharacterType, MessageType, RefreshTokenModel,CustomUser,AiCharacters
# Register your models here.

admin.site.register(LLMServers)
admin.site.register(UserAiCharacter)
admin.site.register(CustomUser)
admin.site.register(AiCharacters)