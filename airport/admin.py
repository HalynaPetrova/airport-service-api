from django.contrib import admin

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Facility,
    Flight,
    Order,
    Route,
    Ticket,
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


admin.site.register(Airport)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Crew)
admin.site.register(Facility)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Route)
admin.site.register(Ticket)
