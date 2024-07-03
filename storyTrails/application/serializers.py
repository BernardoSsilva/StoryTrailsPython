from rest_framework import serializers
from .models import User, Book, Collection
class UserSerializer( serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def validate(self, attrs):
       self._kwargs["partial"] = True
       return super().validate(attrs)
        
class BookSerializer( serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    def validate(self, attrs):
       self._kwargs["partial"] = True
       return super().validate(attrs)
        
        

class CollectionSerializer( serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Collection
        fields = "__all__"    
    def validate(self, attrs):
       self._kwargs["partial"] = True
       return super().validate(attrs)
            