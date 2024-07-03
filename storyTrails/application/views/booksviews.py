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



# * collections endPoints


# * books endPoints

@swagger_auto_schema(
    method='post',
    request_body=BookSerializer(),
    responses={201: BookSerializer(), 400: "bad request", 401:"unauthorized"}
)  
@api_view(["POST"])
def createNewBook(request):
    try:
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms = ["HS256"])        
        if(decodedToken):
            requestBody = {"collection":request.data.get("collection"),"bookName":request.data.get("bookName"),
                           "pagesAmount":request.data.get("pagesAmount"),
                           "concluded":request.data.get("concluded"),
                           "user":decodedToken["id"]}
           
            serializer = BookSerializer(data=requestBody)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response({"details": "unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "bad request"},status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(many=True), 400: "bad request", 401:"unauthorized", 204: "empty content"}
)  
@api_view(["GET"])
def findAllBooks(request):
    try:
        token = request.headers.get("token")
  
        if(not token):
            return Response({"details": "unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
        
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        allBooks = Book.objects.all()
        
        booksSerializer = BookSerializer(allBooks, many=True)
        booksByUser = []
        
        for book in booksSerializer.data:
       
            if(str(book["user"]) == str(decodedToken["id"])):
                booksByUser.append(book)
        
        if(len(booksByUser) > 0):
            return Response(booksByUser, status= status.HTTP_200_OK)
        else:
            return Response({"details": "empty content"},status = status.HTTP_204_NO_CONTENT)
    except:
        return Response({"details": "bad request"},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(many=True), 404: "not found", 401:"unauthorized", 204: "empty content"}
)     
@api_view(["GET"])
def findAllBooksIntoCollection(request, id):
    try:
        token = request.headers.get("token")
  
        if(not token):
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        allBooks = Book.objects.all()
        
        
        booksSerializer = BookSerializer(allBooks, many=True)
        booksByCollection = []
        
        
        for book in booksSerializer.data:
            if(str(book["user"]) == str(decodedToken["id"])):
                if(str(book["collection"] )== str(id)):
                    booksByCollection.append(book)
        
        if(len(booksByCollection) > 0):
            return Response(booksByCollection, status= status.HTTP_200_OK)
        else:
            return Response({"details": "empty content"},status = status.HTTP_204_NO_CONTENT)
    except:
        return Response({"details": "not found"},status=status.HTTP_404_NOT_FOUND)
    
    
@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(many=True), 404: "not found", 401:"unauthorized"}
)     
@api_view(["GET"])
def findBookById(request, id):
    try:
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        
        book = Book.objects.get(pk=id)
        
        if(str(book.user.id) == str(decodedToken["id"])):
            return Response(book, status=status.HTTP_200_OK)
        else:
            return Response({"details": "unauthorized"},status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "not found"},status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='patch',
    request_body=BookSerializer(partial=True),
    responses={200: BookSerializer(), 404: "not found", 401:"unauthorized"}
)  
@api_view(["PATCH"])
def updateBook(request, id):
    try:
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        bookToUpdate = Book.objects.get(pk=id)
        if(str(decodedToken["id"]) == str(bookToUpdate.user.id)):
            serializer = BookSerializer(bookToUpdate,data=request.data ,partial=True)
            print(serializer)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                 return Response({"details": "not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
               
    except:
        return Response({"details": "not found"},status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='delete',
    responses={204: "empty content", 404: "not found", 401:"unauthorized"}
)  
@api_view(["DELETE"])
def deleteBook(request, id):
    try:
        token = request.headers.get("token")
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        bookToDelete = Book.objects.get(pk=id)
        
        if(str(decodedToken["id"]) == str(bookToDelete.user.id)):
            bookToDelete.delete()
            return Response({"details": "empty content"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "unauthorized"},status=status.HTTP_401_UNAUTHORIZED)

    except:
        return Response({"details": "not found"},status=status.HTTP_404_NOT_FOUND)
        
