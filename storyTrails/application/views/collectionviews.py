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


# Endpoint to create a new collection
@swagger_auto_schema(
    method='post',
    request_body=CollectionSerializer(),
    responses={200: CollectionSerializer(), 400: "bad request"}
)  
@api_view(["POST"])
def createNewCollection(request):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        
        # Get the user from the decoded token
        user = User.objects.get(pk=decodedToken["id"])     

        # Get collection details from request data
        collectionName = request.data.get("collectionName")
        collectionObjective = request.data.get("collectionObjective")
        
        # Prepare collection data for serialization
        collectionBody = {"user": user.id, "collectionName": collectionName, "collectionObjective": collectionObjective}
        
        # Serialize the collection data
        serializer = CollectionSerializer(data=collectionBody)
        if serializer.is_valid():
            # Save the new collection if data is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to find all collections
@swagger_auto_schema(
    method='get',
    responses={200: CollectionSerializer(many=True), 204: "empty content", 400: "bad request"}
)
@api_view(["GET"])
def findAllCollections(request):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        
        # Get all collections
        allCollections = Collection.objects.all()
        
        # Serialize all collection objects
        collectionsSerializer = CollectionSerializer(allCollections, many=True)
   
        presenterBody = []
        # Filter collections by user ID from the token
        for collection in collectionsSerializer.data:
            if str(collection["user"]) == str(decodedToken["id"]):
                presenterBody.append(collection)
        
        if presenterBody:
            # Return filtered collections if any, else return empty content
            return Response(presenterBody, status=status.HTTP_200_OK)
        return Response({"details": "Empty content."}, status=status.HTTP_204_NO_CONTENT)
    
    except:
        return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to find a collection by its ID
@swagger_auto_schema(
    method='get',
    responses={200: CollectionSerializer(), 204: "empty content", 404: "not found", 401: "unauthorized"}
) 
@api_view(["GET"])
def findCollectionById(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decoded_token = jwt.decode(token, tokenKey, algorithms=["HS256"])
        
        # Get the collection object by its ID
        collection = Collection.objects.get(pk=id)
        
        # Check if the user ID from the token matches the collection's user ID
        if str(collection.user.id) == str(decoded_token["id"]):
            if collection:
                # Serialize and return the collection data if found
                serializer = CollectionSerializer(collection)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"details": "empty content"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "not found"}, status=status.HTTP_404_NOT_FOUND)


# Endpoint to update a collection
@swagger_auto_schema(
    method='patch',
    request_body=CollectionSerializer(partial=True),
    responses={200: CollectionSerializer(), 400: "bad request", 401: "unauthorized"}
)    
@api_view(["PATCH"])
def updateCollection(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decoded_token = jwt.decode(token, tokenKey, algorithms=["HS256"])
        collectionToAlter = Collection.objects.get(pk=id)
        
        # Check if the user ID from the token matches the collection's user ID
        if str(decoded_token["id"]) == str(collectionToAlter.user.id):
            # Serialize and update the collection data
            serializer = CollectionSerializer(collectionToAlter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to delete a collection
@swagger_auto_schema(
    method='delete',
    responses={202: "collection deleted", 400: "bad request", 401: "unauthorized"}
)      
@api_view(["DELETE"])
def deleteCollection(request, id):
    try:
        # Get the token from request headers
        token = request.headers.get("token")
        # Decode the token to access payload data
        decodedToken = jwt.decode(token, tokenKey, algorithms=["HS256"])
        collectionToDelete = Collection.objects.get(pk=id)
        
        # Check if the user ID from the token matches the collection's user ID
        if str(decodedToken["id"]) == str(collectionToDelete.user.id):
            # Delete the collection if authorized
            collectionToDelete.delete()
            return Response({"details": "collection deleted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"details": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response({"details": "bad request"}, status=status.HTTP_404_NOT_FOUND)
