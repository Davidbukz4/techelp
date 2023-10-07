from django.urls import path
from . import views
#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('about/', views.about),
    path('signup/', views.signup),
    #path('create/', views.create),
]
