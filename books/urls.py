from django.urls import path
from .views import book_view, DetailsPost, buy_book, MyBookListView, donate_book

urlpatterns = [
    path('book/', book_view, name='book_list'),
    path('mybook/', MyBookListView.as_view(), name='my_book'),
    path('book/donate/<int:book_id>/', donate_book, name='donate_book'),
    path('category/<slug:category_slug>/', book_view, name='category_wise_post'),
    path('details/<int:pk>/', DetailsPost.as_view(), name="details_view"),
    path('buy_book/<int:book_id>/', buy_book, name='buy_book'),
]