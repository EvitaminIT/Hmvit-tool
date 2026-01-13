from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import *
from .models import *
from django.http import FileResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication

import string
import secrets

import os

# Create your views here.



def generate_random_code(length=25):
    alphabet = string.ascii_letters + string.digits
    random_code = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_code



def resFun(status, message, data):
    res = Response()
    res.status_code = status
    res.data = {
    'status' : status,
    'message' : message,
    'data' :  data
    }
    return res



# class login_VF(GenericAPIView):
#     serializer_class = loginSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def post(self, request, format=None, *args, **kwargs):
#         print('request', request)
#         serializer = loginSerializer(data=request.data)
#         serializer.is_valid()

#         if not serializer.validated_data:
#             res = resFun(status.HTTP_403_FORBIDDEN, ['email is invalid'], [] )
#             return res

#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']

#         user = authenticate(email=email, password=password)

#         if user is not None:

#             user_role = user.user_role
#             data = toolLink.objects.filter(department = user_role)
#             data = list(data.values())
#             # print(data)

#             res = resFun(status.HTTP_200_OK, ['request successful'], {'j': data[0]['jscode'], 'c' : data[0]['csscode']})

#         else:
#             res = resFun(status.HTTP_400_BAD_REQUEST, ['Email or password is incorrect'], [])
        
#         return res



class login_VF(GenericAPIView):
    serializer_class = loginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return resFun(
                status.HTTP_400_BAD_REQUEST,
                ['Invalid email or password format'],
                []
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(
            request=request,
            username=email,
            password=password
        )

        if user is None:
            return resFun(
                status.HTTP_400_BAD_REQUEST,
                ['Email or password is incorrect'],
                []
            )

        data = toolLink.objects.filter(
            department=user.user_role
        ).values().first()

        
        # print("data pt", data)

        return resFun(
            status.HTTP_200_OK,
            ['request successful'],
            {
                'j': data['jscode'],
                'c': data['csscode']
            }
        )

    

class registration_VF(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None, *args, **kwargs):

        try:
            user = Users.objects.filter(email = request.data.get('email').lower())
            if user.exists():
                res = resFun(status.HTTP_400_BAD_REQUEST,['email already in use'], [])
                return res
        except:
            pass

        try:
            serializer = UserSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                print(serializer.data)
                # serializer.save()

                user = Users(
                    name=request.data.get('name').lower(),
                    user_role=request.data.get('user_role').lower(),
                    email=request.data.get('email').lower(),
                    user_token=generate_random_code(),
                    )
                user.set_password(request.data.get('password'))
                user.save()
                res = resFun(status.HTTP_200_OK, ['user registered'], [])

                    # res = resFun(status.HTTP_400_BAD_REQUEST, 'something went wrong', [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,
                         [ f'{k} - ' + f'{v[0]}' for k,v in serializer.errors.items() ], 
                         ['asdf'])
        except:
            res = resFun(status.HTTP_400_BAD_REQUEST, ['request failed'], [])

            print(serializer.errors.items(),'serializer.errors')
            # for k,v in serializer.errors.items():

        return res
    



# class registration_VF(GenericAPIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         name = request.data.get('name')
#         user_role = request.data.get('user_role')

#         if not email or not password:
#             return resFun(status.HTTP_400_BAD_REQUEST, ['email and password required'], [])

#         email = email.lower()

#         if Users.objects.filter(email=email).exists():
#             return resFun(status.HTTP_400_BAD_REQUEST, ['email already in use'], [])

#         Users.objects.create_user(
#             email=email,
#             password=password,
#             name=name,
#             user_role=user_role,
#             user_token=generate_random_code()
#         )

#         return resFun(status.HTTP_200_OK, ['user registered successfully'], [])


class forget_password_VF(GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request, format=None, *args, **kwargs):


        try:
            user = Users.objects.get(email = request.data.get('email').lower())
            if user:

                message = f'<h4>Hello {user.name},</h4><p>Click here to <a href="http://10.20.40.205:8000/new_password?id={user.id}&token={user.user_token}">reset password</a></p>'
                subject = 'EvTool Reset Password Link!'
                from_email = 'am273.evits@gmail.com'
                recipient_list = [user.email]
                text = 'email sent from MyDjango'

                email = EmailMultiAlternatives(subject, text, from_email, recipient_list)
                email.attach_alternative(message, 'text/html')
                print(email)
                email.send()

                res = resFun(status.HTTP_200_OK,['reset password link has been sent to the email id. Please check you email.'], [])
            else:
                res = resFun(status.HTTP_400_BAD_REQUEST,['no user found.'], [])
            
            return res

        except:
            res = resFun(status.HTTP_400_BAD_REQUEST, ['request failed'], [])


        #     serializer = UserSerializer(data=request.data, partial=True)
        #     if serializer.is_valid():
        #         print(serializer.data)
        #         # serializer.save()

        #         user = Users(
        #             name=request.data.get('name').lower(),
        #             user_role=request.data.get('user_role').lower(),
        #             email=request.data.get('email').lower(),
        #             )
        #         user.set_password(request.data.get('password'))
        #         user.save()
        #         res = resFun(status.HTTP_200_OK, ['user registered'], [])

        #             # res = resFun(status.HTTP_400_BAD_REQUEST, 'something went wrong', [])
        #     else:
        #         res = resFun(status.HTTP_400_BAD_REQUEST,
        #                  [ f'{k} - ' + f'{v[0]}' for k,v in serializer.errors.items() ], 
        #                  ['asdf'])
        # except:
        #     res = resFun(status.HTTP_400_BAD_REQUEST, ['request failed'], [])

        #     print(serializer.errors.items(),'serializer.errors')
            # for k,v in serializer.errors.items():

        return res
    


class generate_new_password_VF(GenericAPIView):
    serializer_class = UserSerializer
    def put(self, request, format=None, *args, **kwargs):
        try:
            id = request.data.get('id') 
            token = request.data.get('token')
            password = request.data.get('password')

            user = Users.objects.get(id=id,user_token=token)

            user.set_password(password)
            user.user_token = generate_random_code()
            user.save()
            res = resFun(status.HTTP_200_OK, ['password updated successfully'], [])

        except:
            res = resFun(status.HTTP_400_BAD_REQUEST, ['request failed'], [])

        return res

    


def templates_VF(request):
    return render(request,'download_templates.html')



def register_VF(request):
    return render(request,'registration.html')


def install_VF(request):
    return render(request, 'install.html')


def installation_guide_VF(request):
    return render(request, 'installation_guide.html')


def new_password_VF(request):

    try:
        id=request.GET.get('id')
        token=request.GET.get('token')

        user = Users.objects.filter(id=id, user_token=token)
        print(user)
        if user.exists():
            return render(request, 'new_password.html', {'user': user})
        else:
            return render(request, 'new_password.html', {'user': 'no_data'})

    except:
        return render(request, 'new_password.html', {'user': 'no_data'})



def reset_password_VF(request):
    return render(request, 'reset_password.html')



def error_form(request):
    return render(request, 'error_form.html')



def download_VF(request, method):

    if method == 'linux':
        file_path = os.path.join(settings.BASE_DIR, 'static/tools/evtool_2.0.zip')
    elif method == 'windows':
        file_path = os.path.join(settings.BASE_DIR, 'static/tools/windows_2.0.zip')

    file_name = os.path.basename(file_path)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f"attachment; filename={file_name}"
    return response 