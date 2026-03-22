from django.shortcuts import render, redirect
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

    


from .models import Book

def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        is_active = request.POST.get("is_active") == "on"

        Book.objects.create(
            title=title,
            author=author,
            is_active=is_active,
            user=request.user  
        )

        return redirect("book_list")

    return render(request, "create_book.html")


def delate(request):
    return render(request, )