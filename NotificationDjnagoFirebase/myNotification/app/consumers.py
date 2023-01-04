# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import threading
import requests
from .models import Notification
from django.contrib.auth.models import User
from multiprocessing import Pool
from asgiref.sync import sync_to_async
from pyfcm import FCMNotification
push_service = FCMNotification(api_key="AAAAOrw_dhM:APA91bG8MxiUIVbVtSwHKZNSw06b8h_fx5E-zX9gBeUaTygHVLtgiMVgDWhiRX_aeHsIPf971wHZM4K8n6auyBKY10pa0EDdWQWAa6Ijr50hguol5Ec7NrhAVg5BA0nm2_c9jgMpz78o")

def send_notification(registration_ids , message_title , message_desc):
    fcm_api = "AAAAOrw_dhM:APA91bG8MxiUIVbVtSwHKZNSw06b8h_fx5E-zX9gBeUaTygHVLtgiMVgDWhiRX_aeHsIPf971wHZM4K8n6auyBKY10pa0EDdWQWAa6Ijr50hguol5Ec7NrhAVg5BA0nm2_c9jgMpz78o"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_desc,
            "title" : message_title,
            "image" : "https://i.ytimg.com/vi/m5WUPHRgdOA/hqdefault.jpg?sqp=-oaymwEXCOADEI4CSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDwz-yjKEdwxvKjwMANGk5BedCOXQ",
            "icon": "https://yt3.ggpht.com/ytc/AKedOLSMvoy4DeAVkMSAuiuaBdIGKC7a5Ib75bKzKO3jHg=s900-c-k-c0x00ffffff-no-rj",
            
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())

def sendNote(regid,message_title,message_body):
    registration_id = regid
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    print(result)

@sync_to_async
def allRegId(username):
    user = User.objects.filter(username=username).first()
    regid = Notification.objects.filter(user=user).first()
    regid = regid.tokenId
    return [regid]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # message = "A new Member Joined the chat"+str(self.room_name)
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        message = text_data_json['message']
        print(threading.get_native_id(),username,message)
        # Send message to room group
        regid = await allRegId(username)
        print("++++++++++++++++++++++")
        print(regid)
        # regid = [regid.tokenId]
        # regid = ['dlVqtUxy3i4QNFQrHePYzY:APA91bFx7BCfzUbow5mjQIO8DynYCP8AWRUWqcUCypk_k3d7kARIZWuGhwJnyTetVifakUs4ywPOoYSFSspz_Tv8tNpRLnDpf2I00YfbhRYpbED2f4Rwkt90TtmBMgdQawAmFq6Ehp2t', 'eWt10vr5u1wuOncXz2z3dO:APA91bGqbAcr0yCVDMCPqv0y10MqNAahLZrqV407eFbUGCa2ckIHcUPUxDN5Gyi7smThL4Ln1bMdj83DajNMwBUdlXfBOAy6wGKYRf4TZhqyEZooxjd0VJSy9vamT2hJTm31sTRooQ0f', 'dlVqtUxy3i4QNFQrHePYzY:APA91bFx7BCfzUbow5mjQIO8DynYCP8AWRUWqcUCypk_k3d7kARIZWuGhwJnyTetVifakUs4ywPOoYSFSspz_Tv8tNpRLnDpf2I00YfbhRYpbED2f4Rwkt90TtmBMgdQawAmFq6Ehp2t']
        send_notification(regid,"you have a notification","heu whatsup!!")
        # sendNote(regid,"you have a notification","heu whatsup!!")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print("+++++++",message)
        username = event['username']
        print("message",threading.get_native_id())
        # Send message to WebSocket
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))