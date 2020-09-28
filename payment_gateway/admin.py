from django.contrib import admin
from .models import *


# Register your models here.
class ordercourses(admin.StackedInline):
    model = OrderCourses
    can_delete = False
    extra = 1
    verbose_name_plural = 'items'
    fk_name = 'order'
    list_select_related = ('order',)
    list_display=('date_added','order','course')
    list_display_links=['date_added','order','course']
class OrderAdmin(admin.ModelAdmin):
    list_display=('customer','price','order_curruncy','date','status')
    inlines = (ordercourses,)
 

admin.site.register(Order,OrderAdmin)