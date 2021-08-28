from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, mixins
from cutomer.serializers.users import *
from rest_framework.authtoken.models import Token
import math
import random
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SignUp(APIView):
    serializer_class = SignupUserSerilizer
    def post(self,request):
        serilize = self.serializer_class(data=request.POST)
        if serilize.is_valid(raise_exception=True):
            user = serilize.save()
            token = token = Token.objects.create(user=user)
            return JsonResponse({"status":"ok","token":token.key})
        else:
            return JsonResponse({"status":"faild"},status=422)