from django.urls import path
from .views import AboutUs

app_name = 'aboutus'

urlpatterns = [
    path('', AboutUs.as_view(), name='aboutus')
]