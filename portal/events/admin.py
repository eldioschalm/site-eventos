# coding: utf-8
from django.contrib import admin
from portal.events.models import Campi
from portal.events.models import Sector
from portal.events.models import Event
from portal.events.models import Programation
from portal.events.models import ProgramationUserExtended


class ProgramationUserExtendedInLine(admin.TabularInline):
    model = ProgramationUserExtended
    extra = 1 #how many rows to show


class ProgramationAdmin(admin.ModelAdmin):
    inlines = (ProgramationUserExtendedInLine,)
    list_per_page = 100


admin.site.register(Campi)
admin.site.register(Sector)
admin.site.register(Event)
admin.site.register(Programation, ProgramationAdmin)