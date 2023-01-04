from django.contrib import admin
from django.urls import path
from .views import sendNoti,chat,showFirebaseJS,loginView,room


urlpatterns = [
    # path('home/',Home.as_view()),
    path('chat/',chat),
    path('send/' , sendNoti.as_view()),
    path('login/',loginView),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('chat/<str:room_name>/<str:username>/', room, name='room'),
]
