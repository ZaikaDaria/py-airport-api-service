from django.contrib import admin

from .models import (
    Flight,
    Route,
    Airport,
    AirplaneType,
    Crew,
    Airplane,
    Order,
    Ticket
)


admin.site.register(Flight)
admin.site.register(Route)
admin.site.register(Airport)
admin.site.register(AirplaneType)
admin.site.register(Crew)
admin.site.register(Airplane)
admin.site.register(Order)
admin.site.register(Ticket)
