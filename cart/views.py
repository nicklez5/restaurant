from pstats import Stats, StatsProfile
from django.http import Http404,JsonResponse
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import HttpResponseNotFound
from .serializers import *
from django.db.models import F,Sum
from .models import *
@api_view(['GET','POST',])
@permission_classes([IsAuthenticated])
def cartitems(request,id):
    if request.method == 'GET':
        cartitemz = CartItem.objects.all()
        serializer = CartItemSerializer(cartitemz,many=True)
        return Response({'CartItem': serializer.data})
    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart = Cart.objects.get(pk=id)
            food = Food.objects.get(pk=request.data['product'])
            cart.ordered_items.add(food)
            cart.save()
            serializer.save()
            return Response({'CartItem': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cartitem(request,id):
    try:
        cartItem = CartItem.objects.get(pk=id)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CartItemSerializer(cartItem)
        return Response({'CartItem': serializer.data})
    elif request.method == 'DELETE':
        cartItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CartItemSerializer(cart,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'CartItem': serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST',])
@permission_classes([IsAuthenticated])
def carts(request):
    if request.method == 'GET':
        carts = Cart.objects.all()
        for i in carts:
            order_items = CartItem.objects.filter(cart=i)
            total = 0
            for x in order_items:
                total = x.quantity * x.product.price + total
            i.total = total
            i.save()
        serializer = CartSerializer(carts,many=True)
        return Response({'Cart': serializer.data})
    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Cart':serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart(request,id):
    try:
        cart = Cart.objects.get(order_user=request.user)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    order_items = CartItem.objects.filter(cart=cart)
    total = 0
    for i in order_items:
        total = i.quantity * i.product.price + total
    cart.total = total
    
    cart.save()
    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response({'Cart': serializer.data})
    elif request.method == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CartSerializer(cart,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Cart':serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
