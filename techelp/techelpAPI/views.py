from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
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
        return Response(serializedItem.validated_data, status.HTTP_201_CREATED)

@api_view()
@permission_classes([IsAuthenticated])
def save(request):
    serializedItem = TicketSerializer(data=request.data)
    serializedItem.is_valid(raise_exception=True)
    ticket = get_object_or_404(Ticket, pk=request.data["id"])
    # write a code to check if user is an IT support
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
    user = request.user
    if user #is IT support group:
        tickets = Ticket.objects.all()
    serializedItem = TicketSerializer(tickets, many=True)
    return render(request, "itsupport.html", serializedItem.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def screenshot(request):
    # write code

@api_view(["GET"])
def search(request):
    # get all user tickets
    ticket_priority = request.query_params.get('priority')
    ticket_status = request.query_params.get('status')
    ticket_category = request.query_params.get('category')
    if ticket_priority:
        # write code
    if ticket_status:
        # write code
    if ticket_category:
        # write code

@api_view()
def login(request):
    email = request.data["email"]
    password = request.data["password"]

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)

    token = Token.objects.get_or_create(user=user)
    response = Response({"token": token.key}, status=status.HTTP_200_OK)

    if user # is in IT support group:
        return redirect("/tickets_admin/")
    else:
        return redirect("/tickets/")

@api_view()
def signout(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if token is None:
        return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

    token_object = Token.objects.get(key=token)
    token_object.delete()
    return redirect("/home")

@api_view()
def home(request):
    # write code here
