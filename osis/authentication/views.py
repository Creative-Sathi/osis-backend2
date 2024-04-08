from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authentication.serializers import *
from django.contrib.auth import authenticate
from authentication.renders import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from authentication.otp import generate,send
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from profileseller.models import Seller


class GetAllUsersView(APIView):
    permission_classes = (AllowAny,) 
    
    def get(self,request,format=None):
        users=User.objects.filter(role='User')
        serializer=GetAllUsersViewSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetBannedUsersView(APIView):
    permission_classes = (AllowAny,) 
    
    def get(self,request,format=None):
        users=User.objects.filter(role='Banned')
        serializer=GetAllUsersViewSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UpdateRoleView(APIView):
    permission_classes = (AllowAny,) 
    
    def put(self, request, id, role, format=None):
        try:
            user = get_object_or_404(User, id=id)
            user.role = role
            user.save()
            return Response({'msg': 'Role Updated Successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other exceptions (if any)
            return Response({'msg': f'Role failed to Update. Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
class GetAllAgentsView(APIView):
    permission_classes = (AllowAny,) 
    
    def get(self,request,format=None):
        users=User.objects.filter(role='Agent')
        serializer=GetAllUsersViewSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


#Generate Token Mannually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#User Registration 
class UserRegistrationView(APIView):
    renderer_classes=[UserRender]
    permission_classes = (AllowAny,)  # Allow any user to access this view
    
    def post(self, request, format=None):
        serializer=UserRegistrationViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            
            token= get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Registration Successful','id':user.id},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
    permission_classes = (AllowAny,) 
     # Allow any user to access this view
    def post(self,request,format=None):
        username=request.data['username']
        password=request.data['password']
        user=authenticate(username=username,password=password)
        if user:
            if check_password(password, user.password):
                role = user.role
                token=get_tokens_for_user(user)
                if role == "Seller":
                    try:
                        seller = Seller.objects.get(seller=user.id)
                    except ObjectDoesNotExist:
                        return Response({'msg':'Form not Submitted','id':user.id},status=status.HTTP_200_OK)

                    if seller.status == "Pending":
                        return Response({'msg':'Your account verification is Under Process'},status=status.HTTP_200_OK)
                    elif seller.status == "Rejected":
                        return Response({'msg':'Your account verification is Rejected'},status=status.HTTP_200_OK)
                    elif seller.status == "Approved":
                        return Response({'token':token,'msg':'Seller Login Successful','role':role,'id':user.id},status=status.HTTP_200_OK)
                elif role == "User":
                    return Response({'token':token,'username':user.username,'msg':'User Login Successful','role':role,'id':user.id},status=status.HTTP_200_OK) 
                elif role == "Agent":
                    return Response({'token':token,'msg':'Agent Login Successful','role':role,'id':user.id},status=status.HTTP_200_OK)
                elif role == "Banned":
                    return Response({'msg':'Your account is Banned'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Invalid Credentials View'},status=status.HTTP_400_BAD_REQUEST)


# User Otp
class UserOtpView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        code=generate()
        send(code,request)
        return Response(data=code,status=status.HTTP_200_OK)
    

# View to Update Password



class UserChangePasswordView(APIView):
    renderer_classes = [UserRender]
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        user_id = request.data['userid']
        password = make_password(request.data['password'])  # Encrypt the password
        
        # Update user password
        try:
            User.objects.filter(id=user_id).update(password=password)
            return Response({'msg': 'Password Change Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Exception error'}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdatePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    
    
    def post(self,request,format=None):
        user_id = request.user.id
        username=request.user.username
        old_password=request.data['oldPassword']
        new_password=request.data['newPassword']
        user=authenticate(username=username,password=old_password)
        new_user = User.objects.get(id=user_id)
        if user:
            user.set_password(new_password)
            user.save()
            return Response({'msg':'Password Updated Successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
        
class GetUserDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,username,format=None):
        user=User.objects.get(username=username)
        serializer=GetUserDetailsViewSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UpdateUserView(APIView):
    permission_classes = (AllowAny,)
    
    def put(self,request,id,format=None):
        user=User.objects.get(id=id)
        print(request.data)
        serializer=UpdateUserDetailsSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)