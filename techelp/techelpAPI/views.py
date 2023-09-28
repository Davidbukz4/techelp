from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
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
    if request.method == "GET":
        # get user id
        # data = {"userID": userID}
        return render(request, "ticket.html", data)
    elif request.method == "POST":
        serializedItem = TicketSerializer(data=request.data)
        serializedItem.is_valid(raise_exception=True)
        serializedItem.save()
        return Response(serializedItem.validated_data, status.HTTP_201_CREATED)

@api_view()
@permission_classes([IsAuthenticated])
def save(request):
    # write code

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tickets(request):
    tickets = # get tickets by user id
    serializedItem = TicketSerializer(tickets)
    return render(request, "enduser.html", serializedItem.data)

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
    # write code

@api_view()
def signout(request):
    # implement signout
