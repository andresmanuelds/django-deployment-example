from django.urls import path
from users_register_app import views

# namespace
app_name = 'users_register_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='registration'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('special/', views.special, name='special'),
]
