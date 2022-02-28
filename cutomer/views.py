from django.views.generic.base import View
from rest_framework.response import Response
from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, mixins
from cutomer.serializers.users import *
from cutomer.serializers.note import *
from rest_framework.authtoken.models import Token
import math
import random
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer



class Index(View):
    def get(self,request):
        
        return render(request,"notepad.html")


# class SignUp(APIView):
#     serializer_class = SignupUserSerilizer
#     def post(self,request):
#         serilize = self.serializer_class(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             user = serilize.save()
#             # token = token = Token.objects.create(user=user)
#             return JsonResponse({"status":"ok"})
#         else:
#             return JsonResponse({"status":"faild"},status=422)
#     def get(self,request):
#         return render(request,"register.html")
# class Login(APIView):
#     def post(self,request):
#         serilize = LoginSerilizer(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             cleaned_data = serilize.validated_data
#             resp,message=cog.login(cleaned_data["username"],cleaned_data["password"])
#             if message == "incorrect":
#                 return Response({"error":True,"message":"username or password invalid"})
#             elif message == "not_cnofirmed":
#                 return Response({"error":True,"message":"username is not confirmed"})
#             else:
#                 access_token = resp['AuthenticationResult']['AccessToken']
#                 response = cog.get_user(access_token)
#
#                 user = User.objects.filter(username=response["email"]).first()
#                 refresh = RefreshToken.for_user(user)
#
#
#                 return Response({"error":False,"data":{
#                     "access_token":str(refresh.access_token),
#                     "refresh":str(refresh)
#                 }})

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serilize = UserSerilizer(request.user)
        return Response(serilize.data)

# class VerifySignup(APIView):
#     def post(self,request):
#         serilize = VerifySerilizer(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             cleaned_data = serilize.validated_data
#             return cog.verify(cleaned_data["username"],cleaned_data["code"])
#     def get(self,request):
#         return render(request,"confirm_email.html")
# class ResendCode(APIView):
#     def post(self,request):
#         serilize = ResendCodeSerilizer(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             cleaned_data = serilize.validated_data
#             return cog.resend_confirmation(cleaned_data["username"])

# class ForgotPassword(APIView):
#     def post(self,request):
#         serilize = ForgotPasswordSerilizer(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             cleaned_data = serilize.validated_data
#             resp = cog.forgot_password(cleaned_data["username"])
#             return resp
#     def get(self,request):
#         return render(request,"forgot_password.html")

# class ConfirmForgotPassword(APIView):
#     def post(self,request):
#         serilize = ConfirmForgotPasswordSerilizer(data=request.POST)
#         if serilize.is_valid(raise_exception=True):
#             cleaned_data = serilize.validated_data
#             resp = cog.confirm_forgot_password(cleaned_data["username"],
#             cleaned_data["password"],
#             cleaned_data["code"])
#             return resp
#     def get(self,request):
#         return render(request,"verify_forgot_password.html")

class CreateNote(APIView):
    permission_classes = [AllowAny]
    def generate_random_string(self,lenght):
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        OTP = ""
        for i in range(lenght):
            OTP += digits[math.floor(random.random() * 62)]
        return OTP
    
    def post(self,request):
        random_string = self.generate_random_string(10)
       
        
        serilize = CreateNoteSerilizer(data={"user":request.user.pk,
        "note":request.POST.get("note",None),
        "random_string":random_string})
        if serilize.is_valid(raise_exception=True):
            note = serilize.save()
            return JsonResponse({"status":"ok","link":note.link()})
        else:
            return JsonResponse({"status":"faild"},status=422)

class ViewNote(APIView):
    def get(self,request,random_string):
        note = get_object_or_404(Note,random_string=random_string)
        return render(request,"show_note.html",context={"note":note})

