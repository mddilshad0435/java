from django.shortcuts import render,redirect
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Notification
from .consumers import sendNote
# class Home(APIView):
#     # permission_classes = IsAuthenticated
#     def get(self,request):
#         user = User.objects.filter(username='admin').first()
#         print(user)
#         send_notification(user_id=user, title="Order Return", message="your message", data=None)
#         return Response({"msg":"Notification send"})


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


@csrf_exempt
@login_required
def chat(request):
    if request.method == 'POST':
        user = request.user
        tokenid = request.POST.get('data')
        # print("+++++++++",user,tokenid)
        userData = Notification.objects.filter(user=user).first()
        if not userData:
            Notification.objects.create(user=user, tokenId=tokenid)
            print("token created---------------")
            return render(request , 'chat.html')
        userData.tokenId = tokenid
        userData.save()
        print("token updated+++++++++++++")
        return render(request , 'chat.html')


    return render(request , 'chat.html')

def room(request, room_name,username):
    print("name",room_name,username)
    return render(request, 'room.html', {
        'room_name': room_name,
        "username": username,
    })

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/chat')
    return render(request, 'login.html')

class sendNoti(APIView):
    def get(self, request):
        # regid = Notification.objects.all().values_list('tokenId')
        # regid = [i[0] for i in regid]
        user = User.objects.filter(username='dilshad').first()
        regid = Notification.objects.filter(user=user).first()
        # resgistration  = ['eWt10vr5u1wuOncXz2z3dO:APA91bHWMcqa6LtmhwUR4zo0QofASfBTYZ6JYhkshS6aonY1lrRPUgqY1uqW9GsVFsqOeMC59cuxrrqDniP4bzwIcmx5_b0ct8jzpKyjQMs9Hjep-XqiarMotBNX_sOsoFSycAviRJnS','dlVqtUxy3i4QNFQrHePYzY:APA91bGG57SPP49vO1rjqVR3RFCvgO4bF4HIFzmW7fPc736x5c1puy6bq4XsqYOJ_kgdzvquJglpCURQvSgvZ6xGYbVOm7N_BF7v7nbQYNPqrjK7f0TydtjKfpRHzjoStQWjoTvBjyq4']
        regid = [regid.tokenId]
        print(regid)
        send_notification(regid , 'Hello this is testing' , 'Hey bro!')
        return HttpResponse("Notification send")



def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCY01qzTxo0UaUKMyt4MLDlfvHfAnBihwA",' \
         '        authDomain: "push-notification-test-4cc97.firebaseapp.com",' \
         '        projectId: "push-notification-test-4cc97",' \
         '        storageBucket: "push-notification-test-4cc97.appspot.com",' \
         '        messagingSenderId: "252266378771",' \
         '        appId: "1:252266378771:web:e238b7b2ddbf55622f31e6",' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")