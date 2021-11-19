from django.urls import path
from .views import AllProduct, DetailProduct, remove_comment


app_name = 'product'

urlpatterns = [
    path('', AllProduct.as_view(), name='all_product'),
    path('product/<int:pk>/<str:slug>', DetailProduct.as_view(), name='detail'),
    path('remove/', remove_comment, name='remove')
]
