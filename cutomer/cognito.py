import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import requests
from base64 import b64encode
from django.conf import settings 
from utils.responses import *


class Cognito:

    

    def __init__(self):
        self.user_pool_id = settings.COGNITO_USER_POOL_ID
        self.client_id = settings.COGNITO_CLIENT_ID
        self.client_secret = settings.COGNITO_CLIENT_SECRET
        self.region = self.user_pool_id.split("_")[0]
        self.aws_access_secret = settings.AWS_ACCESS_SECRET_KEY
        self.aws_key_id = settings.AWS_ACCESS_KRY_ID

        
        
        self.client = boto3.client('cognito-idp',region_name=self.region)
        self.admin_client = boto3.client("cognito-idp",region_name=self.region,aws_access_key_id=self.aws_key_id,aws_secret_access_key= self.aws_access_secret)

 
    def _get_secret_hash(self,username):
        msg = username + self.client_id
        dig = hmac.new(str(self.client_secret).encode('utf-8'), 
            msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2
    def sign_up(self,username,password,name,family_name):
        try:
            resp = self.client.sign_up(
                ClientId=self.client_id,
                SecretHash=self._get_secret_hash(username),
                Username=username,
                Password=password, 
                UserAttributes=[
                {
                    'Name': "name",
                    'Value': name
                },
                {
                    'Name': "family_name",
                    'Value': family_name
                },
                {
                    'Name': "email",
                    'Value': username
                }
                ],
                ValidationData=[
                    {
                    'Name': "email",
                    'Value': username
                },
                {
                    'Name': "custom:username",
                    'Value': username
                }
             ])
        except self.client.exceptions.UsernameExistsException as e:
            return {"error": False, 
                "success": True, 
                "message": "This username already exists", 
                "data": None}
        except self.client.exceptions.InvalidPasswordException as e:
            
            return {"error": False, 
                "success": True, 
                "message": "Password should have Caps,\
                            Special chars, Numbers", 
                "data": None}
        except self.client.exceptions.UserLambdaValidationException as e:
            return {"error": False, 
                "success": True, 
                "message": "Email already exists", 
                "data": None}
        
        except Exception as e:
            return {"error": False, 
                    "success": True, 
                    "message": str(e), 
                "data": None}
        
        return {"error": False, 
                "success": True, 
                "message": "Please confirm your signup, \
                            check Email for validation code", 
                "data": None}
    def verify(self,username,code):
        try:
            response = self.client.confirm_sign_up(
                ClientId=self.client_id,
                SecretHash=self._get_secret_hash(username),
                Username=username,
                ConfirmationCode=code,
                ForceAliasCreation=False,
            ) 
        except self.client.exceptions.UserNotFoundException:
            return error_response(
                code='username_does_not_exist',
                message="Username doesn't exist"
                
            )

        except self.client.exceptions.CodeMismatchException:
            return error_response(
                code='invalid_code',
                message= "Invalid Verification code"
            )
            
        except self.client.exceptions.NotAuthorizedException:
            return error_response(
                code='user_was_confirmed',
                message= "User is already confirmed"
            )
        except self.client.exceptions.ExpiredCodeException:
            return error_response(
                code='expired_code',
                message= "Code has been expired"
            )
        
        except Exception as e:
            return error_response(
                code='error',
                message= f"Unknown error: {e.__str__()}"
            )
        
        return success_response(
            message='Your account is verified successfully'
        )

        
    def resend_confirmation(self,username):
        try:
            response = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                SecretHash=self._get_secret_hash(username),
                Username=username,
            )   
        except Exception as e:
            return error_response(
                code='error',
                message= f"Unknown error: {e.__str__()}"
            )
        
        return success_response(
            message='Code was sent successfully'
        )
    
    def login(self,username,password):
        try:
            resp = self.client.initiate_auth(
                    ClientId=self.client_id,
                    AuthFlow='USER_PASSWORD_AUTH',
                    AuthParameters={
                        'USERNAME': username,
                        'SECRET_HASH': self._get_secret_hash(username),
                        'PASSWORD': password,
                    },
                    ClientMetadata={
                    'username': username,
                    'password': password,
                })
        except self.client.exceptions.NotAuthorizedException:
            return None, "incorrect"
        except self.client.exceptions.UserNotConfirmedException:
            return None, "not_confirmed"
        
        return resp, None


    def sign_in(self,username,password):
        try:
            res = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH':self._get_secret_hash(username)},
                ClientId=self.client_id)
            return(res)
        
        except self.client.exceptions.UserNotFoundException as e:
            return {
                "code":"username_does_not_exist",
                "message": "Username doesn't exists"
            }

        except self.client.exceptions.UserNotConfirmedException as e:
            return {
                "code":"user_is_not_confirmed",
                "message":"User is not confirmed!"
            }

        except Exception as e :
            return {
                "code":"error",
                "message":"Unknown error {e.__str__()}"
            }
    def get_user(self,access_token):
        try:
            res = self.client.get_user(
                AccessToken=access_token
            )
            return self.parse_user_data(res)
        except Exception as e :
            return {
                "code":"error",
                "message":"Unknown error: {e.__str__()}"
            }
            
    def parse_user_data(self,data):
        user_data = {}
        if 'Username' in data and 'UserAttributes' in data :
            user_data['username'] = data['Username']
            for item in data['UserAttributes']:
                user_data[item['Name']] = item['Value']
        return user_data
    
    def authorization(self,code):
        auth_code = self.client_id +":" + self.client_secret
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Authorization' : f'Basic {b64encode(auth_code.encode("utf-8")).decode("utf-8") }'
        }
        params = {
            'grant_type' : 'authorization_code',
            'code' : code ,
            'client_id' : self.client_id,
            'redirect_uri' : self.redirect_uri
        }
        res = requests.post(f'{self.base_url}/oauth2/token',headers = headers , data=params)
        return json.loads(res.content)


    def forgot_password(self,username):
        try:
            response = self.client.forgot_password(
                ClientId=self.client_id,
                SecretHash=self._get_secret_hash(username),
                Username=username,
            )
        except self.client.exceptions.UserNotFoundException:
            return error_response(
                code='username_does_not_exist',
                message= "Username doesn't exist"
            )
            
        except self.client.exceptions.InvalidParameterException:
            return error_response(
                code='user_is_not_confirmed',
                message= f"<{username}> is not confirmed yet"
            )
        
        except self.client.exceptions.CodeMismatchException:
            return error_response(
                code='invalid_verification_code',
                message= "Invalid Verification code"
            )
            
        except self.client.exceptions.NotAuthorizedException:
            return error_response(
                code='user_was_confirmed',
                message= "User is already confirmed"
            )
        
        except Exception as e:
            return error_response(
                code='error',
                message= f"Unknown error: {e.__str__()}"
            )
    

        return success_response(
            message='Please check your Registered email for validation code'
        )
    
    def confirm_forgot_password(self,username,password,code):
        try:
            self.client.confirm_forgot_password(
                ClientId=self.client_id,
                SecretHash=self._get_secret_hash(username),
                Username=username,
                ConfirmationCode=code,
                Password=password,
            )
        except self.client.exceptions.UserNotFoundException as e:
            return error_response(
                code='username_does_not_exist',
                message= "Username doesn't exists"
            )
            
        except self.client.exceptions.CodeMismatchException as e:
            return error_response(
                code='invalid_verification_code',
                message= "Invalid Verification code"
            )
            
        except self.client.exceptions.NotAuthorizedException as e:
            return error_response(
                code='user_was_confirmed',
                message= "User is already confirmed"
            )
        
        except Exception as e:
            return error_response(
                code='error',
                message= f"Unknown error {e.__str__()}"
            )

        return success_response(
            message='Password has been changed successfully'
        )
