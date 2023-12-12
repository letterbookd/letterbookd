import json
from django.shortcuts import render, redirect, get_object_or_404
from reader.models import Reader
from review.models import Review

from library.models import Library, LibraryBook 
from catalog.models import Book

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


from django.core import serializers
from django.urls import reverse
from review.forms import ReviewForm

from django.contrib.auth.decorators import login_required #agar pengguna harus login sebelum mengakses suatu web

# Create your views here.
def show_all_reviews(request):
    # Mengambil semua ulasan dan mengurutkannya berdasarkan tanggal posting dalam urutan menurun (terbaru ke terlama).
    reviews = Review.objects.all().order_by('-date_posted')

    context = {
        'reviews': reviews,
        'page_title': 'All Reviews',
    }
    return render(request, "review_list.html", context)

def show_reviews(request, book_id):
    # TODO: render semua review dari buku
    catalog_book = Book.objects.get(pk=book_id)
    book_title = catalog_book.title
    # Mengambil review dari buku yang sesuai
    reviews = Review.objects.filter(book=catalog_book)

    return render(request, 'review_book.html', {'book_title': book_title, 'reviews': reviews, 'book_id':book_id})

def get_all_user_reviews(request):
    # TODO: mengembalikan json isinya semua review milik Reader
    reader = Reader.objects.get(user = request.user)
    user_review = Review.objects.filter(user = reader)
    return HttpResponse(serializers.serialize('json', user_review), content_type="application/json")

def book_in_library(request, book_id):
    reader = Reader.objects.get(user=request.user)
    library = reader.personal_library
    book = Book.objects.get(pk=book_id)

    target_book = LibraryBook.objects.filter(library=library, book=book)
    return HttpResponse(serializers.serialize('json', target_book), content_type="application/json")

# def get_user_review(request, book_id):
#     # TODO: mengembalikan json review Reader untuk suatu buku
#     certain_review = Review.objects.filter(id=book_id)
#     return HttpResponse(serializers.serialize('json', certain_review))

@csrf_exempt
def edit_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            
            # Periksa apakah pengguna saat ini adalah pemilik review
            if review.user == Reader.objects.get(user=request.user):
                review.stars_rating = request.POST.get("stars_rating")
                review.status_on_review = request.POST.get("status_on_review")
                review.review_text = request.POST.get("review_text")
                review.save()
                print("REVIEWWWWWW BERHASILLLLLLLLLLLLL")
                return HttpResponse("Review berhasil diedit.", status=200)
            else:
                print("GAGALLLLL EDITTTTTTTT")
                return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit review ini.")
        except Review.DoesNotExist:
            print("REVIEWWWWWW GAK ADAAAAAAAAAAAAA")
            return HttpResponseNotFound("Review tidak ditemukan.")
    return HttpResponseNotFound()

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def delete_review(request, review_id):
    # TODO: hapus reviewnya (ajax)
    if request.method == 'DELETE': 
        Review.objects.get(pk=review_id).delete() 
        book = review.book
        reviews = Review.objects.filter(book=book)
        total_rating = 0
        total_reviews = len(reviews)

        for review in reviews:
            total_rating += review.stars_rating

        book.overall_rating = round((total_rating / total_reviews), 2)
        book.save()
        
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

@csrf_exempt
def create_review_ajax(request, book_id):
    if request.method == 'POST':
        print(request.user)
        print(book_id)
        stars_rating = request.POST.get("stars_rating")
        review_text = request.POST.get("review_text")
        book = Book.objects.get(pk=book_id)
        reader = Reader.objects.get(user=request.user)
        reader_library = get_object_or_404(Library, reader__user=request.user)
        try:
            library_book= LibraryBook.objects.get(library=reader_library, book=book)
            status_on_review = library_book.tracking_status
        except LibraryBook.DoesNotExist:
            status_on_review = 0


        new_review = Review(user=reader, book=book, stars_rating=stars_rating, status_on_review=status_on_review, review_text=review_text)
        new_review.save()
        reviews = Review.objects.filter(book=book)
        total_rating = 0
        total_reviews = len(reviews)

        for review in reviews:
            total_rating += review.stars_rating

        book.overall_rating = round((total_rating / total_reviews), 2)
        book.save()

        return HttpResponseRedirect(reverse('review:show_reviews'))

    return HttpResponseNotFound()


#------------------------------------------Flutter Function-----------------------------------#
def show_review_flutter(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_review_flutter(request):
    if request.method == "POST":
        book = review.book
        data = json.loads(request.body)
        # Isi data dr flutter kyk gini
        # data = {
        #     'user':
        #     'stars_rating':
        #     'status_on_review':
        #     'review_text':
        #     'book_id':
        # }
        reader_library = get_object_or_404(Library, reader__user=request.user)
        try:
            library_book= LibraryBook.objects.get(library=reader_library, book=book)
            status_on_review = library_book.tracking_status
        except LibraryBook.DoesNotExist:
            status_on_review = 0

        new_review = Review.objects.create(
            user = Reader.objects.get(user = request.user),
            book = Book.objects.get(pk = data["book_id"]),
            stars_rating = float(data["stars_rating"]),
            status_on_review = status_on_review,
            review_text = data["review_text"],
        )

        new_review.save()
        reviews = Review.objects.filter(book=book)
        total_rating = 0
        total_reviews = len(reviews)

        for review in reviews:
            total_rating += review.stars_rating

        book.overall_rating = round((total_rating / total_reviews), 2)
        book.save()
        return JsonResponse({
            "status": "success",
            "user": Reader.objects.get(user = request.user),
            "book": Book.objects.get(pk = data["book_id"]),
            "stars_rating": data["stars_rating"],
            "status_on_review": data["status_on_review"],
            "review_text": data["review_text"],
        }, status=200)
    
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_review_flutter(request):
    if request.method == 'POST':
        book = review.book
        data = json.loads(request.body)
        # Isi data dr flutter kyk gini
        # data = {
        #     "review_id": 
        # }

        review = Review.objects.get(pk = data["review_id"])
        review.delete()
        reviews = Review.objects.filter(book=book)
        total_rating = 0
        total_reviews = len(reviews)

        for review in reviews:
            total_rating += review.stars_rating

        book.overall_rating = round((total_rating / total_reviews), 2)
        book.save()
        return JsonResponse({"status": True,}, status=200)
    
    return JsonResponse({"status": False}, status=500)

def update_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # data = {
        #     'review_id':
        #     'stars_rating':
        #     'review_text':
        # }

        review = Review.objects.get(pk = data["review_id"])
        review.stars_rating = float(data["stars_rating"])
        review.review_text = data["review_text"]
        review.save()
        
        return JsonResponse({"status": True,}, status=200)
    
    return JsonResponse({"status": False}, status=500)
