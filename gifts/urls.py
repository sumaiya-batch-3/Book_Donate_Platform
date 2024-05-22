from django.urls import path
from .views import book_view,redeem_book

urlpatterns = [
    path('book_view', book_view, name='book_wise_post'),
    path('redeem_book/<int:book_id>/', redeem_book, name='redeem_book'),
]
