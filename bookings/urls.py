from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('my-bookings/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]
