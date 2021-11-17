from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','password2']
        extra_kwargs={'password':{'write_only':True}}
    def validate(self,data):
        email=data['email']
        password=data['password']
        password2=data['password2']
        print(email,password,password2)
        if password != password2:
            raise serializers.ValidationError({'error':'Password must be same'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'User with this email is already Registered'})
        return data
    # def save(self): # need to implement it as password 2 needs to be save
    #     pass