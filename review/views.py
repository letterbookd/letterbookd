from django.shortcuts import render, redirect
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
    all_review = Review.objects.all()
    return HttpResponse(serializers.serialize('json', all_review))

def book_in_library(request, id):
    reader = Reader.objects.get(user=request.user)
    library = reader.personal_library
    book = Book.objects.get(pk=id)

    target_book = LibraryBook.objects.filter(library=library, book=book)
    return HttpResponse(serializers.serialize('json', target_book))

# def get_user_review(request, book_id):
#     # TODO: mengembalikan json review Reader untuk suatu buku
#     certain_review = Review.objects.filter(id=book_id)
#     return HttpResponse(serializers.serialize('json', certain_review))

@csrf_exempt
def create_review_ajax(request, book_id):
    form = ReviewForm(request.POST)
    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.user = request.user
        review.save()
        return HttpResponseRedirect(reverse('review:show_reviews'))
    
    context = {'form': form}

    if request.method == 'POST':
        stars_rating = request.POST.get("stars_rating")
        review_text = request.POST.get("review_text")
        book = Book.objects.get(pk=book_id)
        reader = Reader.objects.get(user=request.user)
        library = Library.objects.get(user=request.user, book=book)
        status_on_review = library.status_tracking

        new_review = Review(user=reader, book=book, stars_rating=stars_rating, status_on_review=status_on_review, review_text=review_text)
        new_review.save()

        response_data = {
            'review_id': new_review.id,
            'user': new_review.user.username,
            'stars_rating': new_review.stars_rating,
            'status_on_review': new_review.status_on_review,
            'review_text': new_review.review_text,
            'book_id': new_review.book_id,
            'success': True
        }

        return JsonResponse(response_data, status=201)

    return HttpResponseNotFound()

        # # Mengambil status pelacakan (tracking status) dari objek Library
        # book = Book.objects.get(pk=book_id)
        # library_book = Library.objects.get(library=)


        # new_review = Review.objects.create(user=user, stars_rating=stars_rating, status_on_review=status_on_review, review_text=review_text, book_id=book_id)
        # new_review.save()

        # Membuat respons JSON yang berisi data review dan status_on_review


def edit_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            
            # Periksa apakah pengguna saat ini adalah pemilik review
            if review.user == request.user:
                review.stars_rating = request.POST.get("stars_rating")
                review.status_on_review = request.POST.get("status_on_review")
                review.review_text = request.POST.get("review_text")
                review.save()
                return HttpResponse("Review berhasil diedit.", status=200)
            else:
                return HttpResponseForbidden("Anda tidak diizinkan untuk mengedit review ini.")
        except Review.DoesNotExist:
            return HttpResponseNotFound("Review tidak ditemukan.")
    return HttpResponseNotFound()



def delete_review(request, review_id):
    # TODO: hapus reviewnya (ajax)
    if request.method == 'DELETE': 
        Review.objects.get(pk=review_id).delete() 
        return HttpResponse(b"DELETED", status=201)
    return HttpResponseNotFound()

def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, review_id):
    data = Review.objects.filter(pk=review_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
