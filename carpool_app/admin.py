from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Car)
admin.site.register(Location)
admin.site.register(LuggageSize)
admin.site.register(Profile)
admin.site.register(MemberCar)
admin.site.register(Ride)
admin.site.register(RequestRide)