from django.urls import path, include
from .views import home_page, pricing_page

app_name = 'main'

urlpatterns = [
    path('', home_page, name='home'),
    path('pricing/', pricing_page, name='pricing'),
]
