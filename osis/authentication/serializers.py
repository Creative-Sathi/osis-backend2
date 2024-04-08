from django.forms import ValidationError
from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model,authenticate



class UserRegistrationViewSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name','username', 'password','role','password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        attrs['username'] = username
        
        return attrs
    
    def create(self, validated_data):
      return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user.password != password:
                raise serializers.ValidationError('Invalid Credentials')
            else:
                return serializers.ValidationError('User is not active')
            
            # user = authenticate(username=username,password=password)
            # if not user:
            #     raise serializers.ValidationError('Invalid Credentials')
            # if not user.is_active:
            #     raise serializers.ValidationError('User is not active')
        else:
            raise serializers.ValidationError('Username and Password are required')

        attrs['username'] = username
        
        return attrs

User = get_user_model()

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def update(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class GetAllUsersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','username']
        
class GetUserDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','username']
        
class UpdateUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        