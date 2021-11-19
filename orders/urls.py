from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('active/', views.Order.as_view(), name='active'),
    path('complete/', views.CompleteOrder.as_view(), name='complete_order'),
    path('add/<int:id>', views.add_order, name='add_order'),
    path('plus/<int:id>', views.plus_order, name='plus_order'),
    path('minus/<int:id>', views.minus_order, name='minus_order'),
    path('remove/<int:id>', views.remove_order, name='remove_order'),
]
