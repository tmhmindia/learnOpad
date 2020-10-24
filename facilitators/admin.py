from django.contrib import admin
from .models import *
from LandingPage.admin import *
from mailing.views import *
from django.contrib import messages
from django.contrib.auth.models import Group

class ExperienceInline(admin.StackedInline):
    model = Experience
    can_delete = False
    verbose_name_plural = 'Experience'
    fk_name = 'facilitator'
class FacilitatorQueriesInline(admin.StackedInline):
    model = FacilitatorQueries
    can_delete = False
    verbose_name_plural = 'Facilitator queries'
    fk_name = 'user'
class ApplicantsAdmin(admin.ModelAdmin):
    inlines = (ExperienceInline,FacilitatorQueriesInline )
    list_display=('Aid','name','user','phone','intrest','status')
    list_select_related = ('facilitator', 'experience')
    list_display_links=['name','user','phone','intrest','status']
    search_fields = ( 'name',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ApplicantsAdmin, self).get_inline_instances(request, obj)
    def approve_facilitator(self,request , queryset):
       
        for user in queryset:
            check=None
            try:
                check=Facilitator.objects.get(user=user)
            except:
                check=None
            if check is None:
                facilitator=Facilitator.objects.create(name=user.name,phone=user.phone,user=user)
                facilitator.save()
                user.status='Approved'
                group = Group.objects.get(name='Facilitators')
                user.user.groups.add(group)
                user.save()
                successOnRegistration(user.user)
                messages.success(request, (user.name+' is approved !'))
            else:
                user.status='Approved'
                user.save()
                messages.info(request, (check.name+' is already approved !'))
        
    def shortlisted_facilitator(self,request , queryset):
        li=[]
        for applicant in queryset:
            if applicant.status=='Shortlisted':
                messages.error(request, (applicant.name+' is already shortlisted !'))
            else:
                applicant.status='Shortlisted'
                applicant.save()
                li.append(applicant.user.email)
                successOnShortlisted(applicant.user)
                messages.info(request, (applicant.name+' is  shortlisted !'))
            

       
    def OnHold_facilitator(self,request , queryset):
        for applicant in queryset:
            if applicant.status=='On Hold':
                messages.error(request, (applicant.name+' is already On Hold !'))
            else:
                applicant.status='On Hold'
                applicant.save()
                messages.info(request, (applicant.name+' is  On Hold !'))
                
        
    def Rejected_facilitator(self,request , queryset):
         for applicant in queryset:
            if applicant.status=='Rejected':
                messages.error(request, (applicant.name+' is already Rejected !'))
            else:
                applicant.status='Rejected'
                applicant.save()
                messages.info(request, (applicant.name+' is Rejected !'))
    
    OnHold_facilitator.short_description = 'On Hold'
    Rejected_facilitator.short_description = 'Rejected'        
    shortlisted_facilitator.short_description = 'Shortlisted'       
    approve_facilitator.short_description = 'Approve'
    actions = [approve_facilitator, shortlisted_facilitator, OnHold_facilitator, Rejected_facilitator]


# class ExperienceAdmin(admin.ModelAdmin):
#     list_display=('Eid','Linkedin_Url','Website_Url','Youtube_Url','RExperience','TExperience','facilitator')
# class FacilitatorQueriesAdmin(admin.ModelAdmin):
#     ist_display=('Qid','query','status','user')
class FacilitatorAdmin(admin.ModelAdmin):
    list_display=('Fid','name','DOB','phone','PAddress','TAddress','profile','Bio','country','state','zipcode','user')
    inlines = (offer_inline,)
    list_display_links=['name','DOB','phone','PAddress','TAddress','profile','Bio','country','state',]
admin.site.register(Facilitator,FacilitatorAdmin)
admin.site.register(Applicants,ApplicantsAdmin)
admin.site.register(OTP)

