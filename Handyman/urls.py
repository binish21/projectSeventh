from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('register', views.register.as_view(), name="register"),
    path('login', views.login, name="login,"),
    path('profile/<int:id>', views.profile.as_view(), name="profile"),

]