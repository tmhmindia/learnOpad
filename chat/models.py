from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Group
from chat.middileware import RequestMiddleware
from tmhm_host import settings
from django.core.cache import cache 
import datetime
from django.utils import timezone
from myauth.models import *


User = get_user_model()
class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    status=models.BooleanField(default=False,null=True,blank=True)

    
class ChatGroup(Group):
    """ extend Group model to add extra info"""
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat:room', args=[str(self.id)])
    def get_group_receiver(self):
        users=self.user_set.all()
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request

        if request.user.email == users[0].email:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        return receiver.first_name+" "+receiver.last_name
    def get_group_receiver_id(self):
        users=self.user_set.all()
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request

        if request.user.email == users[0].email:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        return receiver.id
    def get_group_receiver_profileUrl(self):
        users=self.user_set.all()
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request

        if request.user.email == users[0].email:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        url=None
        if receiver.groups.filter(name='Learners').exists():
            url=receiver.learner.profile.url
        if receiver.groups.filter(name='Facilitators').exists():
            url=receiver.user.facilitator.profile.url
        return url
    def get_group_sender_profileUrl(self):
        users=self.user_set.all()
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request

        if request.user.email == users[0].email:
            sender=users[0]
            receiver=users[1]
        else:
            sender=users[1]
            receiver=users[0]
        url=None
        if sender.groups.filter(name='Learners').exists():
            url=receiver.learner.profile.url
        if sender.groups.filter(name='Facilitators').exists():
            url=receiver.user.facilitator.profile.url
        return url
        


class Message(models.Model):
    author = models.ForeignKey(CustomUser, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField(default=None,null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    chatgroup=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
    seen =models.BooleanField(default=False,null=True,blank=True)
    blob=models.FileField(default=None,null=True,blank=True)

    

    def __str__(self):
        return self.author.email

    def last_10_messages(self):
        
        return Message.objects.filter(chatgroup=self).order_by('timestamp')
