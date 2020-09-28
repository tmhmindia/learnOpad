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

def some_view():
    template = get_template('html/shortlisted.html')
    image_url ="static/email/Registration.png"
    context = Context({'image_name':image_url})
    content=render_to_string('html/shortlisted.html')
    #content = template.render()
    subject='nothing'
    # if not user.email:
    #     raise BadHeaderError('No email address given for {0}'.format(user))
    msg = EmailMessage(subject, content, 'vijaygwala97@gmail.com', to=['vijaygwala73@gmail.com',])
    res=msg.send()
    return HttpResponse('%s'%res)

#speed up mails
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()


# inform about facilitator registration
def RegistrationSuccessAdminEmail(name,catlist):
    subject = 'About collaboration'
    message = name+""" Wants to collaborate With Us and Showing Intrest in """+catlist
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['vijaygwala97@gmail.com',]
    mymail( subject, message, email_from, recipient_list ,fail_silently=False)
    





# the function for sending an email
def send_email(subject, text_content, html_content=None, sender=None, recipient=None, image_path=None, image_name=None):
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=sender, to=recipient if isinstance(recipient, list) else [recipient])
    
    if all([html_content,image_path,image_name]):
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = 'html'  # set the primary content to be text/html
        email.mixed_subtype = 'related' # it is an important part that ensures embedding of an image 

        with open(image_path, mode='rb') as f:
            image = MIMEImage(f.read())
            
            image.add_header('Content-ID', f"<{image_name}>")
            email.attach(image)
    EmailThread(email).start()
from LandingPage.models import Course  
def registration(request):
    course=Course.objects.all()
    context={'images':course}
    return render(request,'html/shortlisted.html',context)

def successOnRegistration(to,template):
    recipient = [to]
    sender =settings.EMAIL_HOST_USER # 
    image_path = Path.cwd() / 'static' / 'email'/template
    image_name = Path(image_path).name
    

    subject = "Thankyou for Becoming a ChangeMaker"
    context={
        'image_name':image_name
     }
    text_message = f"Email with a nice embedded image {image_name}."
   
    html_message=render_to_string('html/before_payment.html',context)
#     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient, image_path=image_path, image_name=image_name)


def successOnShortlisted(recipient_list,template):
    
    recipient = recipient_list
    sender =settings.EMAIL_HOST_USER # 
    image_path = Path.cwd() / 'static' / 'email'/template
    image_name = Path(image_path).name
    

    subject = "Thankyou for Becoming a ChangeMaker"
    context={
        'image_name':image_name
     }
    text_message = f"Email with a nice embedded image {image_name}."
   
    html_message=render_to_string('html/shortlisted.html',context)
#     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient, image_path=image_path, image_name=image_name)


