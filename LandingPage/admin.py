from django.contrib import admin
from .models import *

# By vijay
admin.AdminSite.site_title = "TMHM PVT LTD"
#admin.AdminSite.index_title = ""
admin.AdminSite.site_header = "TMHM PVT LTD "
#admin.AdminSite.login_template='admin_login.html'
#endVijay

# Register your models here.
# from .models import Signup , OnlineCounselling
# admin.site.register(Signup)
# admin.site.register(OnlineCounselling)
class offer_inline(admin.TabularInline):
    model = offer
    verbose_name_plural = 'Offerd By'
    extra = 1
class CourseVideoInline(admin.StackedInline):
    model = CourseVideo
    can_delete = False
    extra = 1
    verbose_name_plural = 'Preview'
    fk_name = 'course'
    list_select_related = ('course',)
    list_display=('Vid','title','description','session_duration','video','course')
    list_display_links=['title','description','session_duration','video','course']
class CategoryAdmin(admin.ModelAdmin):
    list_display=('cat_id','name')
    list_display_links=['name']
class SubCategoryAdmin(admin.ModelAdmin):
    list_display=('subCat_id','name','cat_id')
    list_display_links=['name','cat_id']
class CourseAdmin(admin.ModelAdmin):
    list_display=('Cid','code','title','days','months','description','subCat_id')
    inlines = (offer_inline,CourseVideoInline)
    list_display_links=['code','title']
# class offerAdmin(admin.ModelAdmin):
#     list_display=('Fid','Cid')

class CouncellingAdmin(admin.ModelAdmin):
    list_display=('councelling_id','name','email','phone_number')
    list_display_links=['name','email','phone_number']


class LiveSessionsAdmin(admin.ModelAdmin):
    list_display=('Vid','title','description','session_duration','session_start','session_end','video','course')
class AudienceAdmin(admin.ModelAdmin):
    list_display=('audience',)
class QueryAdmin(admin.ModelAdmin):
    list_display=('Fid','query','reply')
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','categories','mobile','message')
class CorporateTalksAdmin(admin.ModelAdmin):
    list_display=('name','email','mobile','company_name','training_need','message','city','state','check')


admin.site.register(LiveSession,LiveSessionsAdmin)
admin.site.register(OnlineCounsellingDetails,CouncellingAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Course,CourseAdmin)
# admin.site.register(offer,offerAdmin)
admin.site.register(Audience,AudienceAdmin)
admin.site.register(ContactUs,ContactAdmin)
admin.site.register(CorporatesTalks,CorporateTalksAdmin)
admin.site.register(Rating)
