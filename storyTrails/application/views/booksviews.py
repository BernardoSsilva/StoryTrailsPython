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

# Get the token key from environment variables
tokenKey = os.environ.get("TOKEN_KEY")

# * collections endPoints


# * books endPoints
# create new book endPoint
@swagger_auto_schema(
    method='post',
    request_body=BookSerializer(),
    responses={201: BookSerializer(), 400: "bad request", 401:"unauthorized"}
)  
@api_view(["POST"])
def createNewBook(request):
    try:
        # Get the token from request headers
        token = request.headers.get("token")

        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms = ["HS256"])        
        if(decodedToken):
            # Extract data from request body and assign to a dictionary
            requestBody = {"collection":request.data.get("collection"),
                           "bookName":request.data.get("bookName"),
                           "pagesAmount":request.data.get("pagesAmount"),
                           "concluded":request.data.get("concluded"),
                           "user":decodedToken["id"]}

            # Create a serializer for data manipulation based on the request body dictionary
            serializer = BookSerializer(data=requestBody)

            # Check data validity and save if valid
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# Find all books endpoint
@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(many=True), 400: "bad request", 401:"unauthorized", 204: "empty content"}
)  
@api_view(["GET"])
def findAllBooks(request):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
  
        if(not token):
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        allBooks = Book.objects.all()
        
        # Serialize all book objects
        booksSerializer = BookSerializer(allBooks, many=True)
        booksByUser = []
        
        # Filter books by user ID from the token
        for book in booksSerializer.data:
            if(str(book["user"]) == str(decodedToken["id"])):
                booksByUser.append(book)
        
        # Return the filtered books if any, else return empty content
        if(len(booksByUser) > 0):
            return Response(booksByUser, status= status.HTTP_200_OK)
        else:
            return Response({"details": "empty content"}, status = status.HTTP_204_NO_CONTENT)
    except:
        return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# Find all books in a collection endpoint
@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(many=True), 404: "not found", 401:"unauthorized", 204: "empty content"}
)     
@api_view(["GET"])
def findAllBooksIntoCollection(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
  
        if(not token):
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        allBooks = Book.objects.all()
        
        # Serialize all book objects
        booksSerializer = BookSerializer(allBooks, many=True)
        booksByCollection = []
        
        # Filter books by user ID from the token and collection ID
        for book in booksSerializer.data:
            if(str(book["user"]) == str(decodedToken["id"])):
                if(str(book["collection"]) == str(id)):
                    booksByCollection.append(book)
        
        # Return the filtered books if any, else return empty content
        if(len(booksByCollection) > 0):
            return Response(booksByCollection, status= status.HTTP_200_OK)
        else:
            return Response({"details": "empty content"}, status = status.HTTP_204_NO_CONTENT)
    except:
        return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)


# Find book by ID endpoint
@swagger_auto_schema(
    method='get',
    responses={200: BookSerializer(), 404: "not found", 401:"unauthorized"}
)     
@api_view(["GET"])
def findBookById(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        
        # Get the book object by its ID
        book = Book.objects.get(pk=id)
        
        # Check if the user ID from the token matches the book's user ID
        if(str(book.user.id) == str(decodedToken["id"])):
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)


# Update book endpoint
@swagger_auto_schema(
    method='patch',
    request_body=BookSerializer(partial=True),
    responses={200: BookSerializer(), 404: "not found", 401:"unauthorized"}
)  
@api_view(["PATCH"])
def updateBook(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        bookToUpdate = Book.objects.get(pk=id)
        
        # Check if the user ID from the token matches the book's user ID
        if(str(decodedToken["id"]) == str(bookToUpdate.user.id)):
            serializer = BookSerializer(bookToUpdate, data=request.data, partial=True)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)


# Delete book endpoint
@swagger_auto_schema(
    method='delete',
    responses={204: "empty content", 404: "not found", 401:"unauthorized"}
)  
@api_view(["DELETE"])
def deleteBook(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        bookToDelete = Book.objects.get(pk=id)
        
        # Check if the user ID from the token matches the book's user ID
        if(str(decodedToken["id"]) == str(bookToDelete.user.id)):
            bookToDelete.delete()
            return Response({"details": "empty content"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)
