from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from cutomer.models import *

# class SignupUserSerilizer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     def create(self, validated_data):
#
#         cognito = co.Cognito()
#         result = cognito.sign_up(validated_data['username'],
#         validated_data['password'],
#         validated_data['first_name'],
#         validated_data['last_name'])
#         print(result)
#         if result["error"] == False:
#             user = User.objects.create_user(username=validated_data['username'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'])
#             return user
#         else:
#             return None
#
#     class Meta:
#         model = User
#         fields = ("first_name","last_name","username","password")

class SigninUserSerilizer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        return user
    class Meta:
        model = User
        fields = ("username","password")

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","last_name","username"]


class VerifySerilizer(serializers.Serializer):
    code = serializers.CharField()
    username = serializers.EmailField()

class ResendCodeSerilizer(serializers.Serializer):
    username = serializers.EmailField()

class LoginSerilizer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

class ForgotPasswordSerilizer(serializers.Serializer):
    username = serializers.EmailField()

class ConfirmForgotPasswordSerilizer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()
    code = serializers.CharField()