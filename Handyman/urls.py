from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('register', views.register.as_view(), name="register"),
    path('login', views.login.as_view(), name="login"),
    path('profile/<int:id>', views.profile.as_view(), name="profile"),
    path('dashboard/<int:id>', views.dashboard.as_view(), name="dashboard"),
    path('contract/<int:id>', views.contract.as_view(), name="contract")

]