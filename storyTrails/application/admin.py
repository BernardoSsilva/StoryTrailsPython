from django.contrib import admin
from .models import Book, Collection, User
# Register your models here.

admin.site.register(User)
admin.site.register(Collection)

admin.site.register(Book)
