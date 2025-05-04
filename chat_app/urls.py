"""
URL configuration for chat_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from api.views import RegisterUser, GetDataAndCreateUserChatModel, GetAccessTokenApi, GetDiscoversData, \
    ConnectToAiCharacter, Tryapi, GetChatListView, GetRoomchats

urlpatterns = [
    path("admin/", admin.site.urls),
    path("registerUser",RegisterUser.as_view()),
    path("getDataAndCreateUserChatModel",GetDataAndCreateUserChatModel.as_view()),
    path("getAccessTokenApi",GetAccessTokenApi.as_view()),
    path("getDiscoversData",GetDiscoversData.as_view()),
    path("connect-to-aichat",ConnectToAiCharacter.as_view()),
    path("getRoomchats",GetRoomchats.as_view()),
    path("getChatListView",GetChatListView.as_view()),
    path("tryapi",Tryapi.as_view()),

]
