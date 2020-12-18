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
def successOnRegistration(user):
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
        
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
    
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


# inform about facilitator registration
def RegistrationSuccessAdminEmail(name,catlist):
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':"This is to notify that "+ name +" has completed the registration process and the interested areas are "+ catlist +". Please check the facilitator 's profile and revert back to the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CorporateCampusToAdminEmail(org,orgname):
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"Vijay Gwala",
        'msg':orgname+" has requested for the "+org.course.title+" course. Acknowledge their request and attach a payment link to it as a further step."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
# when course is created bt not approved
def CourseCreationEmailToAdmin(course):
    subject = 'About Course creation'
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay Gwala",
        'msg':'''The course '''+course.offering.all()[0].name + '''have created on the LearnOpad Platform is successfully uploaded and therefore open to interested aspirants to enroll.
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
        'msg':'''The course '''+course.offering.all()[0].name + '''have created on the LearnOpad Platform is successfully Approved therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : The course code provided above is unique to his '''+ course.title +''' course, you can use that unique code to edit your course. Don't share it with anyone.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CourseApprovalEmailToFacilitator(course):
    sender = settings.EMAIL_HOST_USER
    recipient = [course.offering.all()[0].user.user.email,]
    context={
        'name':course.offering.all()[0].name,
        'msg':'''The course you have created on the LearnOpad Platform is successfully Approved and therefore open to interested aspirants to enroll.
Course name : '''+course.title+'''
Course code : '''+course.code+'''
NOTE : Your request for course approval is accepted and now your course is live on our learnOpad platform and open for the enrolment. 
Please be ready with the schedule and the required PPTs/documents.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


# when course is created bt not approved 
def CourseCreationEmailToFacilitator(course):
    sender = settings.EMAIL_HOST_USER
    recipient = [course.offering.all()[0].user.user.email,]
    context={
        'name':course.offering.all()[0].name,
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
    sender = settings.EMAIL_HOST_USER
    recipient = [user.email,]
    context={
        'name':user.first_name+" "+user.last_name,
        'msg':"This mail is intended to notify you that your subscription has been successful. You have been provided with access to handle and explore the dashboard of the facilitator."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def ToAdminSuccessfullSubscriptionOfFacilitator(subscription_plan):
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay"+" "+"Gwala",
        'msg':subscription_plan.user.get_full_name()+" has successfully subscribed for this "+subscription_plan.plan+" and can access the facilitator dashboard."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def CourseRejection(course):
    sender = settings.EMAIL_HOST_USER
    recipient = [course.offering.all()[0].user.user.email,]
    context={
        'name':course.offering.all()[0].name,
        'msg':'''Thank you for showing efforts and requesting for '''+ course.title +'''course creation.
However, we can't approve your course because we already have similar courses on our platform. Please review your courses and submit again.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
def ToAdminDeleteCourseVideo(video):
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay"+" "+"Gwala",
        'msg':video.course.offering.all()[0].name+" has deleted "+ video.title +" video from "+ video.course.title+ " course."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
def ToAdminUploadCourseVideo(video):
    sender = settings.EMAIL_HOST_USER
    recipient = ['vijaygwala97@gmail.com',]
    context={
        'name':"vijay"+" "+"Gwala",
        'msg':video.course.offering.all()[0].name+" has Uploaded "+ video.title +" video from "+ video.course.title+ " course."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def LearnerSuccessfullSubscription(enroll):
    sender = settings.EMAIL_HOST_USER
    recipient = [enroll.Lid.user.email,]
    context={
        'name':enroll.Lid.name,
        'msg':'''Congratulations on enrolling in '''+ enroll.Cid.title +''' Good to see your inclination towards learning and enhancing your skill set. Hope you enjoy the course and learning with us!
                            you can use to open your course on your Learner's dashboard.'''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)


def ToAdminLearnerSuccessfullSubscription(enroll):
    sender = settings.EMAIL_HOST_USER
    recipient = ["vijaygwala97@gmail.com",]
    context={
        'name':"vijay gwala",
        'msg':enroll.Lid.name+''' has successfully enrolled for '''+ enroll.Cid.title +''' course of '''+enroll.Cid.offering.all()[0].name
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def ToAdminContactUsQuery(contactus):
    sender = settings.EMAIL_HOST_USER
    recipient = ["vijaygwala97@gmail.com",]
    context={
        'name':"vijay gwala",
        'msg':contactus.name +''' has filled ContactUs form and the query is   
        " '''+contactus.message+''' " ''' 
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def ToAdminGiveStaffPrivilages(staff):
    sender = settings.EMAIL_HOST_USER
    recipient = ["vijaygwala97@gmail.com",]
    context={
        'name':"vijay gwala",
        'msg':"You have approved "+staff.get_full_name() +" to access the admin panel and use the privileges."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def ToStaffGiveStaffPrivileges(staff):
    sender = settings.EMAIL_HOST_USER
    recipient = [staff.user.email,]
    context={
        'name':staff.user.get_full_name(),
        'msg':'''Congratulations you have been approved to access the admin privileges.
Below is your Credentials.
email : '''+staff.user.email+'''
password : '''+staff.user.password
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)
def ToLearnerForCertificate(certificate):
    sender = settings.EMAIL_HOST_USER
    recipient = [certificate.learner.user.email,]
    context={
        'name':certificate.learner.name,
        'msg':'''Congratulations! You’ve successfully completed '''+ certificate.course.title +''' On behalf of LearnOpad we are pleased to issue your official Introduction to CSS3 Certificate.
    Now that you’ve earned your Certificate, why not share it with your network?
    Ways to share:
    Add your '''+certificate.course.title+''' Certificate directly to your LinkedIn profile
Download PDF to print or share
Share on social media and your LinkedIn Feed
Once again, congratulations on your achievement.
Keep it up, '''
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def ToAdminCouncellingDetail(councelling):
    sender = settings.EMAIL_HOST_USER
    recipient = ["vijaygwala97@gmail.com",]
    context={
        'name':"vijay gwala",
        'msg':'''There is a request for counselling. Below are the details refer them and proceed accordingly.
              name :  '''+councelling.name+ '''
              phone : '''+councelling.phone_number+'''
              email : '''+councelling.email
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)

def FacilitatorApprovalWithoutSubscription(applicant):
    sender = settings.EMAIL_HOST_USER
    recipient = [applicant.user.email,]
    context={
        'name':applicant.name,
        'msg':"Congratulations. Let's begin your journey with LearnOpad Platform. You are approved to access the facilitator dashboard and create your courses."
     }
    text_message = f"Email with a nice embedded image {context.get('name')}."
   
    html_message=render_to_string('html/email_template.html',context)
     
    send_email(subject="TMHM PVT LTD", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient)





def SHORTLIST(request):
    id=request.POST.get('id',None)
    user=CustomUser.objects.get(id=int(id))
    successOnShortlisted(user)
    return JsonResponse({'name':user.get_full_name()})