from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
]
