from django.contrib import admin
from .models import AirplanesData, AirportsData, BoardingPasses, Bookings, \
    Flights, Routes, Seats, Segments, Tickets

# Register your models here.
admin.site.register(AirplanesData)
admin.site.register(AirportsData)
admin.site.register(BoardingPasses)
admin.site.register(Bookings)
admin.site.register(Flights)
admin.site.register(Routes)
admin.site.register(Seats)
admin.site.register(Segments)
admin.site.register(Tickets)
