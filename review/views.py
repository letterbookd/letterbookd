from django.shortcuts import render

from review.models import Review
from library.models import Library 
from catalog.models import Book
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.urls import reverse

from django.contrib.auth.decorators import login_required #agar pengguna harus login sebelum mengakses suatu web
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def show_reviews(request, book_id):
    # TODO: render semua review dari buku
    catalog_book = Book.objects.get(id=book_id)
    book_title = catalog_book.title
    # Mengambil review dari buku yang sesuai
    reviews = Review.objects.filter(book_id=book_id)

    return render(request, 'review_list.html', {'book_title': book_title, 'reviews': reviews})

def get_all_user_reviews(request):
    # TODO: mengembalikan json isinya semua review milik Reader
    all_review = Review.objects.all()
    return HttpResponse(serializers.serialize('json', all_review))

def get_user_review(request, book_id):
    # TODO: mengembalikan json review Reader untuk suatu buku
    certain_review = Review.objects.filter(id=book_id)
    return HttpResponse(serializers.serialize('json', certain_review))

@csrf_exempt
def create_review(request, book_id):
    if request.method == 'POST':
        user = request.user
        stars_rating = request.POST.get("stars_rating")
        review_text = request.POST.get("review")

        # Mengambil status pelacakan (tracking status) dari objek Library
        library = Library.objects.get(user=user, book_id=book_id)
        status_on_review = library.status_tracking

        new_review = Review.objects.create(user=user, stars_rating=stars_rating, status_on_review=status_on_review, review_text=review_text, book_id=book_id)
        new_review.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def edit_review(request, review_id):
    # TODO: edit reviewnya (ajax)
    if request.method == 'POST':
        review = Review.objects.get(review_id) 
        review.stars_rating = request.POST.get("stars_rating")
        review.status_on_review = request.POST.get("status_on_review")
        review.review_text = request.POST.get("review")
        review.save()
        return HttpResponse(b"EDITED", status=201)
    return HttpResponseNotFound()


def delete_review(request, review_id):
    # TODO: hapus reviewnya (ajax)
    if request.method == 'DELETE': 
        Review.objects.get(pk=review_id).delete() 
        return HttpResponse(b"DELTED", status=201)
    return HttpResponseNotFound()

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")