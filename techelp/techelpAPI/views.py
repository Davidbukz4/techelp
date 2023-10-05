from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
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
from django.utils import timezone
#from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create(request):
    if request.method:
        data = request.data.copy()
        data["owner"] = request.user.id
        #tickets = Ticket.objects.filter(owner=request.user)
        serializedItem = TicketSerializer(data=data)
        if serializedItem.is_valid():
            serializedItem.save()
            return JsonResponse({"message": "Ticket created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": serializedItem.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status.HTTP_405_METHOD_NOT_ALLOWED)

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
        return JsonResponse({"message": "User is already authenticated"}, status=status.HTTP_200_OK)

    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        
        enduser = get_object_or_404(Enduser, email=email)
        itsupport = get_object_or_404(ITSupport, email=email)

        if enduser.check_password(password):
            user = authenticate(email=email, password=password)

            if user is None:
                login(request, user)
                token, created = Token.objects.get_object_or_404(user=user)
                return JsonResponse({"message": "User logged in successfully", "user_id": user.id, "token": token.key}, status=status.HTTP_200_OK)
                #return redirect("/tickets")
        elif itsupport.check_password(password):
            user = authenticate(email=email, password=password)

            if user is None:
                login(request, user)
                token, created = Token.objects.get_object_or_404(user=user)
                return JsonResponse({"message": "User logged in successfully", "user_id": user.id, "token": token.key, "role": "admin"}, status=status.HTTP_200_OK)
                #return redirect("/tickets_admin")
        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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
                return redirect("/tickets/?arg={logged_user}")
            else:
                it_support = ITSupport.objects.create(username, email, password)
                user = authenticate(email=email, password=password)
                login(request, user)
                return redirect("/tickets_admin")
    else:
        form = UserCreationForm()
        return render(request, "signup.html", {"form": form})
