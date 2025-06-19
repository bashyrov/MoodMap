from django.urls import path
from .views import registration, login_view
from .users_functionality.mood_funcs import chat_view, diary_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registration/', registration, name='registration'),
    path('chat/', chat_view, name='chat'),
    path('diary/', diary_view, name='diary'),
]

