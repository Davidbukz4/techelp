from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from .models import Enduser, ITSupport, Ticket
from .serializers import EnduserSerializer, ITSupportSerializer, TicketSerializer
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
#from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create(request):
    user_id = request.user.id
    tickets = Ticket.objects.filter(owner=request.user)
    serializedItem = TicketSerializer(tickets)
    if request.method == "GET":
        return render(request, "ticket.html", serializedItem.data)
    elif request.method == "POST":
        serializedItem = TicketSerializer(data=request.data)
        serializedItem.is_valid(raise_exception=True)
        serializedItem.save()
        #return Response(serializedItem.validated_data, status.HTTP_201_CREATED)
        return redirect("/tickets")

@api_view()
@permission_classes([IsAuthenticated])
def save(request):
    serializedItem = TicketSerializer(data=request.data)
    serializedItem.is_valid(raise_exception=True)
    ticket = get_object_or_404(Ticket, pk=request.data["id"])
    if request.user.groups.filter(name="IT_Support").exists():
        ticket.status = request.data["status"]
        ticket.save()
        return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(owner=user)
    serializedItem = TicketSerializer(tickets, many=True)
    return render(request, "enduser.html", serializedItem.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tickets_admin(request):
    #user = request.user
    #if user #is IT support group:
    tickets = Ticket.objects.all()
    serializedItem = TicketSerializer(tickets, many=True)
    return render(request, "itsupport.html", serializedItem.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def screenshot(request):
    pass

@api_view(["GET"])
def search(request):
    # get all user tickets
    ticket_priority = request.query_params.get('priority')
    ticket_status = request.query_params.get('status')
    ticket_category = request.query_params.get('category')
    if ticket_priority:
        pass
    if ticket_status:
        pass
    if ticket_category:
        pass

@api_view()
def login(request):
    if request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        form = UserCreationForm(data=request.data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)

    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)

    token = Token.objects.get_or_create(user=user)
    response = Response({"token": token.key}, status=status.HTTP_200_OK)

    if request.user.groups.filter(name="IT_Support").exists():
        return redirect("/tickets_admin")
    else:
        authenticated__user = Enduser.objects.get(email=form.cleaned_data["email"])
        tickets = Ticket.objects.filter(owner=authenticated__user)
        serializedItem = TicketSerializer(tickets, many=True)
        return render(request, "enduser.html", serializedItem.data)

@api_view()
def signout(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is None:
        return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

    token_object = Token.objects.get(key=token)
    token_object.delete()
    logout(request)
    return redirect("/home")

@api_view(["POST"])
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            user = form.save()
            if request.POST.get("role") == "enduser":
                enduser = Enduser.objects.create(username, email, password)
                logged_user = enduser
                user = authenticate(email=email, password=password)
                login(request, user)
                return redirect("/?arg={logged_user}")
            else:
                it_support = ITSupport.objects.create(username, email, password)
                user = authenticate(email=email, password=password)
                login(request, user)
                return redirect("/tickets_admin")
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})
