from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login-signup/', views.login_register_user, name="login-signup"),
    path('logout/', views.logout_user, name="logout"),
    path('details/', views.AccountView.as_view(), name="details"),
    path('history/', views.OrderHistoryView.as_view(), name="history"),

]
