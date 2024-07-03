from django.urls import path
from . import views
from .views import userviews,  booksviews, collectionviews

urlpatterns = [
    
    # * Users endpoints
    path('users/find/all', userviews.getAllUsers, name="findAllUsers"),
    path('users/find/<str:id>', userviews.getById, name="findUserById"),
    path("users/create", userviews.createUser, name="createUser"),
    path("users/edit/<str:id>", userviews.updateUser, name="editUser"),
    path("users/delete/<str:id>", userviews.deleteUser, name="deleteUser"),
    path("users/login", userviews.authenticate, name="loginUser"),
    
    # * Collections endpoints
    path("collections/find/all", collectionviews.findAllCollections, name="findAllCollections"),
    path("collections/create", collectionviews.createNewCollection, name="createNewCollection"),
    path("collections/find/<str:id>", collectionviews.findCollectionById, name="findOneCollection"),
    path("collections/edit/<str:id>", collectionviews.updateCollection, name="editCollection"),
    path("collections/delete/<str:id>", collectionviews.deleteCollection, name="deleteCollection"),

    # * Books endpoints
    
    path("books/create", booksviews.createNewBook, name="createNewBook"),
    path("books/find/all", booksviews.findAllBooks, name="findAllBooks"),
    path("books/find/collection/<str:id>", booksviews.findAllBooksIntoCollection, name="findAllBooksIntoCollection"),
    path("books/find/<str:id>", booksviews.findBookById, name="findBookBydId"),
    path("books/edit/<str:id>", booksviews.updateBook, name="updateBook"),
    path("books/delete/<str:id>", booksviews.deleteBook, name="deleteBook")
]