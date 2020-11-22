from django.contrib import admin
from .models import *

# Register your models here.
class CorporatesAdmin(admin.ModelAdmin):
    list_display=('name','email','organization','course')
    list_display_links=('name','email','organization','course')
admin.site.register(CorporatesTalks,CorporatesAdmin)


