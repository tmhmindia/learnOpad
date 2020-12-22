from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import json
from .models import *
import sys
from chat.utils import * 
from django.template.loader import render_to_string
from myauth.models import *




User = get_user_model()

class ChatConsumer(WebsocketConsumer):
   
    def fetch_messages(self, data):
        group=ChatGroup.objects.get(id=self.room_name)
        messages = Message.last_10_messages(group)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
    
    def get_group_receiver(self,obj):
        users=CustomUser.objects.filter(groups__name=obj.name)
        user = self.scope['user']
        
        if user.email == users[0].email:
            sender=users[0]
            receiver=users[1]
        else:
            
            sender=users[1]
            receiver=users[0]
    
        return receiver

    def new_message(self, data):
        author = data['from']
        author_user = CustomUser.objects.filter(email=author)[0]
        chatgroup=ChatGroup.objects.get(id=self.room_name)
        if data['message']:
            message = Message.objects.create(
            author=author_user, 
            content=data['message'],chatgroup=chatgroup)
        else:
            message = Message()
            message.author=author_user
            message.chatgroup=chatgroup
            message.blob.save(data['blob']['filename'],data['blob']['file_content'])
            message.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)  
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        if message.author.groups.filter(name="Learners").exists():
            url=message.author.learner.profile.url
        else:
            url=message.author.user.facilitator.profile.url
        if message.blob :
            return {
            'author': message.author.email,
            'content': message.content,
            'timestamp': str(timezone.localtime(message.timestamp)),
            'blob':message.blob.url,
            'group_id':message.chatgroup.id,
            'profile_url':url
        }
        else:
            return {
            'author': message.author.email,
            'content': message.content,
            'timestamp': str(timezone.localtime(message.timestamp)),
            'blob':'null',
            'group_id':message.chatgroup.id,
            'profile_url':url
        }

    commands = {
        'new_message': new_message,
        'fetch_messages': fetch_messages
        
    }
    
    def update_user_status(self, user, status):
        user=UserProfile.objects.get(user = user)
        #print(user)
        user.status=status
        user.save()
        return user
    
    def send_status_connect(self):
        chatgroup=ChatGroup.objects.get(id=self.room_name)
        receiver=self.get_group_receiver(chatgroup)
        flag=receiver.profile.status
        status=None
        if flag:
            status='online'
            html_status='<p> (Online) </p>'

        else:
            status='offline'
            html_status='<p> (Offline) </p>'
        message={
            'html_status':html_status,
            'status':status,
            'receiver_id':str(receiver.id)
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def send_status_disconnect(self):
        chatgroup=ChatGroup.objects.get(id=self.room_name)
        receiver=self.get_group_receiver(chatgroup)
        flag=receiver.profile.status
       
        status=None
        if flag:
            status='offline'
            html_status='<p> (Offline) </p>'
      
           
        else:
            status='online'
            html_status='<p> (Online) </p>'

        message={
            'html_status':html_status,
            'status':status
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        user = self.scope ['user']
        if user.is_authenticated:
            self.update_user_status(user, True)
            self.send_status_connect()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope ['user']
        if user.is_authenticated:
            print("disconnect")
            self.update_user_status(user, False)
            self.send_status_disconnect()
    def receive(self,text_data=None,bytes_data=None):
        data={}
        filename=None
        if text_data:
            ext=text_data
            if ext.split(".")[-1] in ['jpg','png','pdf','jpeg','zip','txt']:
                print(text_data+" "+"filename")
                self.scope['session']['filename']=text_data
                self.scope['session'].save()
            else:
               
                data = json.loads(text_data)
                data['blob']=bytes_data
                self.commands[data.get('command')](self, data)
        
        if (bytes_data):    
            data['blob']=BytesToFile(bytes_data,self.scope['session'].get('filename'))
            data['message']=None
            
            data['from']=self.scope["user"]
            self.commands['new_message'](self, data)
            
        
        
        

    
        
           
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))


    def chat_message(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps(message))
        
    
       
        
