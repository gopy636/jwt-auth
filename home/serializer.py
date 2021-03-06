
from rest_framework import serializers
from .models import *

class LoginSerializers(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=50)


class CustmUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=['email','name','phone','password']

    