from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.response import Response

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")
