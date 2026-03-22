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

        # ✅ create book first
        book = Book.objects.create(
            title=title,
            author=author,
            is_active=is_active,
            user=request.user
        )

        # ✅ now book exists → safe to use
        image_file = fetch_book_image(title)

        if image_file:
            book.image.save(f"{title}.jpg", image_file, save=True)

        return redirect("book_list")

    return render(request, "create_book.html")


def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('book_list')


def fetch_book_image(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    response = requests.get(url)
    data = response.json()

    try:
        img_url = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        img_response = requests.get(img_url)
        return ContentFile(img_response.content)
    except:
        return None