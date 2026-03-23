from django.urls import path
from . import views


urlpatterns = [
    path('create_book/', views.create_book, name='create_book'),
    path('book_list/', views.book_list, name='book_list'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    ]