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
from django.http import HttpResponse

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
    
    # if all([html_content,image_path,image_name]):
    #     email.attach_alternative(html_content, "text/html")
    #     email.content_subtype = 'html'  # set the primary content to be text/html
    #     email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image 

    #     with open(image_path, mode='rb') as f:
    #         image = MIMEImage(f.read())
            
    #         image.add_header('Content-ID', f"<{image_name}>")
    #         email.attach(image)
    EmailThread(email).start()

def successOnRegistration(user,msg):
    recipient = ['vijaygwala97@gmail.com','l.gouri1234@gmail.com']
    sender =settings.EMAIL_HOST_USER # 
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"This is to inform you that your registration process with the LearnOpad E-learning platform has been successful. Our team will send you an email shortly, if you are shortlisted, after checking your profile, which will allow you to access and explore the Facilitators dashboard."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
#     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


def successOnShortlisted(user):
    
    recipient = ['vijaygwala97@gmail.com','l.gouri1234@gmail.com']
    sender =settings.EMAIL_HOST_USER # 
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"We are pleased to inform you that we have reviewed your profile and shortlisted you as a facilitator. We are extremely pleased with this collaboration and look forward to your long-term commitment to our organization. ",
        'link':'https://www.learnopad.com/create_order'
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
#     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


# inform about facilitator registration
def RegistrationSuccessAdminEmail(name,catlist):
    subject = 'About collaboration'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':"This is to notify "+ name +" ,registration process for "+ catlist +" on LearnOpad has been successfully completed. Please check the facilitator 's profile and revert back to the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CourseCreationEmailToAdmin(Course):
    subject = 'About Course creation'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':"This is to notify "+ name +" ,registration process for "+ catlist +" on LearnOpad has been successfully completed. Please check the facilitator 's profile and revert back to the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CourseCreationEmailToFacilitator(Course):
    subject = 'About Course Creation'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':"This is to notify "+ name +" ,registration process for "+ catlist +" on LearnOpad has been successfully completed. Please check the facilitator 's profile and revert back to the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
