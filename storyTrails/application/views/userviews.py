from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
import jwt
from ..models import User, Book, Collection
from ..serializers import BookSerializer, CollectionSerializer, UserSerializer
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

tokenKey = os.environ.get("TOKEN_KEY")


tokenKey = os.environ.get("TOKEN_KEY")
# * user endPoints
@swagger_auto_schema(
    method='get',
    responses={200: UserSerializer(many=True), 400:"Bad request", 204:"no content"}
)
@api_view(["GET"])
def getAllUsers(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        if(len(serializer.data) > 0):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"details":"no content"},status=status.HTTP_204_NO_CONTENT)
    except:    
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: UserSerializer(), 404:"not found"}
)
@api_view(["GET"])
def getById(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
         
        return Response(serializer.data, status=status.HTTP_200_OK)
    except: 
        return Response({"details":"user not found"},status=status.HTTP_404_NOT_FOUND)
         

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: UserSerializer(), 400: 'Bad Request'}
)
@api_view(["POST"])
def createUser(request):
    try:
        serializer = UserSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST) 
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='patch',
    request_body=UserSerializer(partial=True),
    responses={202: UserSerializer(), 401: 'Unauthorized',404:"not found"}
)
@api_view(["PATCH"])
def updateUser(request, id):
    try:
        updatedUser = User.objects.get(pk=id)
        print(updatedUser)
        serializer =  UserSerializer(updatedUser, data=request.data, partial=True)
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        if(str(decodedToken["id"]) == str(updatedUser.id)):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else: 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='delete',
    responses={202: "user deleted", 401: 'Unauthorized',404:"not found"}
)
@api_view(["DELETE"])
def deleteUser(request, id):
    try:
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        deletedUser = User.objects.get(pk=id)
        if(str(decodedToken["id"]) == str(deletedUser.id)):
            deletedUser.delete()
            return Response({"details": "user deleted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"details": "Unauthorized"},status=status.HTTP_401_UNAUTHORIZED)       
    except:
        return Response({"details": "not found"},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer(partial=True),
    responses={200: UserSerializer(), 401: "Invalid credentials.",404:"not found",400:"User login and password are required."}
)
@api_view(["POST"])
def authenticate(request):
    try:
        user_login = request.data.get("userLogin")
        password = request.data.get("userPassword")

        if not user_login or not password:
            return Response({"detail": "User login and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(userLogin=user_login)
        userDict = user.to_dict()
       
        if(password == userDict["userPassword"]):
            token = jwt.encode({"id": userDict["id"]},tokenKey,  algorithm="HS256")
            serializer = UserSerializer(user)
            return Response({"token": token, "user":serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    except:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    