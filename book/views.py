from django.shortcuts import render, redirect
from .models import Book
from django.shortcuts import get_object_or_404
import requests
from django.core.files.base import ContentFile
from .models import Book

# Create your views here.


def book_list(request):
    print(request, request.user)
    if not request.user.is_authenticated:
        return redirect("login")
    


    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'book_list.html', {'books': books})

    




def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        is_active = request.POST.get("is_active") == "on"

       
        book = Book.objects.create(
            title=title,
            author=author,
            is_active=is_active,
            user=request.user
        )

      
        image_file = fetch_book_image(title, author)
        

        if image_file:
            book.image.save(f"{title}.jpg", image_file, save=True)

        return redirect("book_list")

    return render(request, "create_book.html")


def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('book_list')


def fetch_book_image(title, author):
    query = f"{title}+inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

    response = requests.get(url)
    data = response.json()

    try:
        image_url = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        image_response = requests.get(image_url)
        return ContentFile(image_response.content)
    except:
        return None


def edit_book(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.save()
        return redirect("book_list")

    return render(request, "create_book.html", {"book": book})