from django.urls import path
from . import views

urlpatterns = [
    # Hotel
    path('', views.hotel_list, name='hotel_list'),
    path('add/', views.add_hotel, name='add_hotel'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    # Room
    path('<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('<int:hotel_id>/rooms/add/', views.add_room, name='add_room'),
    # Booking
    path('room/<int:room_id>/book/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # Admin bookings
    path('admin/bookings/', views.all_bookings, name='all_bookings'),
    path('admin/bookings/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    # Payment
    path('booking/<int:booking_id>/pay/', views.make_payment, name='make_payment'),
    path('payment/<int:payment_id>/receipt/', views.view_receipt, name='view_receipt'),
    path('payment/<int:payment_id>/receipt/pdf/', views.download_receipt_pdf, name='download_receipt_pdf'),
    # Review
    path('hotels/<int:hotel_id>/review/', views.add_review, name='add_review'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
