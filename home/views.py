
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from .models import *
from .threads import *
from home.serializer import *


class SignupAPI(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer=CustmUserSerializer(data=data)
            if serializer.is_valid():
                name = serializer.data["name"]
                email = serializer.data["email"]
                password = serializer.data["password"]
                if CustomUser.objects.filter(email=email).first():
                    return Response({"status":400, "result":"Acount already exists."})
                else:
                    tok = str(uuid.uuid4())
                    new_user = CustomUser.objects.create(email=email, name=name, verification_token=tok)
                    new_user.set_password(password)
                    thread_obj = send_verification_email(email, tok)
                    thread_obj.start()
                    new_user.save()
                    return Response({"status":200, "result":"Account created, verification mail sent", "data":serializer.data})
            return Response({"status":400, "error":serializer.errors})
        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})



class VerifyUserAPI(APIView):
    def get(self, request, token):
        try:
            data = request.data
            user_obj = CustomUser.objects.filter(verification_token = token).first()
            if user_obj:
                if user_obj.is_verified:
                    return Response({"status":400, "result":"Account is already verified"})
                user_obj.is_verified = True
                user_obj.save()
                return Response({"status":200, "result":"Account verification successfull"})
        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})

    
class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializers(data=data)
            if serializer.is_valid():
                email = serializer.data["email"]
                password = serializer.data["password"]
                print(email,password)
                cust_obj = CustomUser.objects.filter(email=email).first()
                print(cust_obj)
                if cust_obj is None:
                    return Response({"status":400, "result":"Account does not exist"})
                if not cust_obj.is_verified:
                    return Response({"status":400, "result":"Email not verified. Check your mail"})
                user = authenticate(email=email, password=password)
                jwt_token = RefreshToken.for_user(user)
                return Response({"status":200, "result":"Login successfully", "token":str(jwt_token.access_token)})
            return Response({"status":400, "error":serializer.errors})
        except Exception as e:
            print(e)
        return Response({"status":500, "message":"something went wrong"})

  
    