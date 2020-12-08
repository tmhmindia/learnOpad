from django.shortcuts import render,redirect
from django.core.mail import send_mail as mymail
from django.conf import settings
from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
import threading
from django.http import HttpResponse ,JsonResponse
from myauth.models import *

#speed up mails
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()

# the function for sending an email
def send_email(subject, text_content, html_content=None, sender=None, recipient=None, image_path=None, image_name=None):
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=sender, to=recipient if isinstance(recipient, list) else [recipient])
    email.attach_alternative(html_content, "text/html")
    email.content_subtype = 'html'  # set the primary content to be text/html
    EmailThread(email).start()
# After successfull Registration
def successOnRegistration(user,msg):
    recipient = [user.email,]
    sender =settings.EMAIL_HOST_USER # 
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"This is to inform you that your registration process with the LearnOpad E-learning platform has been successful. Our team will send you an email shortly, if you are shortlisted, after checking your profile, which will allow you to access and explore the Facilitators dashboard."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
    
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

# After shortlisting an applicant
def successOnShortlisted(user):
    
    recipient = [user.email,]
    sender =settings.EMAIL_HOST_USER # 
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"We are pleased to inform you that we have reviewed your profile and shortlisted you as a facilitator. We are extremely pleased with this collaboration and look forward to your long-term commitment to our organization. ",
        'link':'https://www.learnopad.com/create_order'
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
    
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


# inform about facilitator registration
def RegistrationSuccessAdminEmail(name,catlist):
    subject = 'About collaboration'
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':"This is to notify "+ name +" ,registration process for "+ catlist +" on LearnOpad has been successfully completed. Please check the facilitator 's profile and revert back to the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CorporateCampusToAdminEmail(org):
    subject = 'About Training'
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':org.organization+" has asked for the "+org.course.title+" course. Acknowledge their request and attach a payment link to it as a further step."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
# when course is created bt not approved
def CourseCreationEmailToAdmin(Course):
    subject = 'About Course creation'
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay Gwala",
        'msg':'''The course '''+course.offering.all[0].name + '''have created on the LearnOpad Platform is successfully uploaded and therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : The course code provided above is unique to his '''+ course.title +''' course, you can use that unique code to edit your course. Don't share it with anyone.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
def CourseApprovalEmailToAdmin(Course):
    subject = 'About Course Approval'
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay Gwala",
        'msg':'''The course '''+course.offering.all[0].name + '''have created on the LearnOpad Platform is successfully Approved therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : The course code provided above is unique to his '''+ course.title +''' course, you can use that unique code to edit your course. Don't share it with anyone.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CourseApprovalEmailToFacilitator(Course):
    subject = 'About Course Creation'
    sender = settings.EMAIL_HOST_USER
    recipient = [course.offering.all[0].user.user.email,]
    context={
        'name':course.offering.all[0].name,
        'msg':'''The course you have created on the LearnOpad Platform is successfully Approved and therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : The course code provided above is unique to your '''+ course.title +''' course, you can use that unique code to edit your course. Don't share it with anyone.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


# when course is created bt not approved 
def CourseCreationEmailToFacilitator(Course):
    subject = 'About Course Creation'
    sender = settings.EMAIL_HOST_USER
    recipient = [course.offering.all[0].user.user.email,]
    context={
        'name':course.offering.all[0].name,
        'msg':'''The course you have created on the LearnOpad Platform is successfully uploaded and therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : The course code provided above is unique to your '''+ course.title +''' course, you can use that unique code to edit your course. Don't share it with anyone.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

# Successfull Facilitator Subscription 
def FacilitatorSuccessfullSubscription(user):
    subject = 'Thank You for Subscription'
    sender = settings.EMAIL_HOST_USER
    recipient = [user.email,]
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"This mail is intended to notify you that your subscription has been successful. You have been provided with access to handle and explore the dashboard of the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def SHORTLIST(request):
    id=request.POST.get('id',None)
    user=CustomUser.objects.get(id=int(id))
    successOnShortlisted(user)
    return JsonResponse({'name':user.get_full_name})