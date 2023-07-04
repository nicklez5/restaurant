from django.shortcuts import render
from django.contrib.auth.models import update_last_login
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView 
from rest_framework import generics, status 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser 
from .serializers import UserChangePasswordSerializer, UserSerializer, UserLoginSerializer, RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
     if request.method == 'GET':
          queryset = CustomUser.objects.all()
          serializer = UserSerializer(queryset,many=True)
          return Response(serializer.data)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        reg_serializer = RegisterSerializer(data=request.data)
        data = {}
        if reg_serializer.is_valid():
            CustomUser = reg_serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = CustomUser.email
            data['username'] = CustomUser.username
            token = Token.objects.get(user=CustomUser).key
            data['token'] = token
        else:
            data = reg_serializer.errors
        return Response(data)
@api_view(['POST'])
@permission_classes([AllowAny])
def enter(request):
    
    if request.method == 'POST':
         serializer_class = UserLoginSerializer(data=request.data)
         serializer_class.is_valid(raise_exception=True)
         user = serializer_class.validated_data['user']
         #token, created = Token.objects.get_or_create(user=user)
         return Response({
             #'token'  : token.key,
             'user_id': user.pk,
            'email': user.email
         })
@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def users(request,id):
        try:
            custom_user = CustomUser.objects.get(pk=id)
        except custom_user.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        if(request.method) == 'GET':
            serializer = UserSerializer(custom_user)
            return Response(serializer.data)
        elif(request.method) == 'DELETE':
            custom_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
        try:
            custom_user = CustomUser.objects.get(pk=id)
        except custom_user.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not custom_user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            custom_user.set_password(serializer.data.get("new_password"))
            custom_user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
     permission_classes = (IsAuthenticated,)
     def get(self,request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    
# Create your views here.
