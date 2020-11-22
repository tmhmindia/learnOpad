from django.contrib import admin
from .models import *

# Register your models here.
class CampusAdmin(admin.ModelAdmin):
    list_display=('name','email','campus','course')
    list_display_links=('name','email','campus','course')
admin.site.register(Campus,CampusAdmin)

