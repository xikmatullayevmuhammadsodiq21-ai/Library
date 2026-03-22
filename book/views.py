from django.shortcuts import render, redirect
from .models import Book
from django.shortcuts import get_object_or_404
import requests
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

    


from .models import Book

def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        is_active = request.POST.get("is_active") == "on"
        image_url = fetch_book_cover(title)

        Book.objects.create(
            title=title,
            author=author,
            is_active=is_active,
            user=request.user,  
            image_url=image_url
        )

        return redirect("book_list")

    return render(request, "create_book.html")


def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    return redirect('book_list')


def fetch_book_cover(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"

    try:
        response = requests.get(url)
        data = response.json()

        if "items" in data:
            book = data["items"][0]
            image = book["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            return image
    except:
        pass

    return None