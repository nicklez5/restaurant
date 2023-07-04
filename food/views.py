from pstats import Stats, StatsProfile
from django.http import Http404,JsonResponse
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import HttpResponseNotFound
from .serializers import *
from .models import *
@api_view(['GET','POST',])
@permission_classes([AllowAny])
def foods(request):
    if request.method == 'GET':
        foodz = Food.objects.all()
        serializer = FoodSerializer(foodz,many=True)
        return Response({'Foods': serializer.data})
    elif request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Foods': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def food(request,id):
    try:
        data = Food.objects.get(id=id)
    except Food.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FoodSerializer(data)
        return Response({'Food':serializer.data})
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.methnod == 'POST':
        serializer = FoodSerializer(data,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Food':serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
