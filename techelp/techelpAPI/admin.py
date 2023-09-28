from django.contrib import admin
from .models import Enduser, ITSupport, Ticket

admin.site.register(Enduser)
admin.site.register(ITSupport)
admin.site.register(Ticket)
