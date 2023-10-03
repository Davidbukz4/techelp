from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('home/', views.home),
    path('', views.tickets),
    path('tickets-admin/', views.tickets_admin),
    path('create/', views.create),
    path('view-screenshot/', views.screenshot),
    path('search/', views.search),
    path('save/', views.save),
    path('signout/', views.signout),
    path('login/', views.login),
]

