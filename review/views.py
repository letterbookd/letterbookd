from django.shortcuts import redirect, render

from review.models import Review
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_reviews(request, book_id):
    # TODO: render semua review dari buku
    reviews = Review.objects.filter (book_id = book_id)
    return render (request, 'main.html', {'reviews': reviews})

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
    # TODO: bikin review baru (ajax)
    if request.method == 'POST':
        user = request.user
        stars_rating = request.POST.get("stars_rating")
        status_on_review = request.POST.get("status_on_review")
        review_text = request.POST.get("review")

        new_review = Review.objects.create(user=user, stars_rating=stars_rating, status_on_review=status_on_review, review_text=review_text, book_id=book_id)
        new_review.save()
        return JsonResponse(new_review, status=201)
    return HttpResponseNotFound()

def edit_review(request, review_id):
    # TODO: edit reviewnya (ajax)
    if request.method == 'POST':
        review = Review.objects.get(review_id) 
        review.stars_rating = request.POST.get("stars_rating")
        review.status_on_review = request.POST.get("status_on_review")
        review.review_text = request.POST.get("review")
        review.save()
    return HttpResponse("Review berhasil diedit")

def delete_review(request, review_id):
    # TODO: hapus reviewnya (ajax)
    review = Review.objects.get(id=review_id) 
    review.delete()
    return redirect('main:show_main')