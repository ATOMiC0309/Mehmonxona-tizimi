from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Hotel, Room, Booking, Payment, Review
from .forms import HotelForm, RoomForm, BookingForm, PaymentForm, ReviewForm, UserRegistrationForm
from .utils import render_to_pdf
from django.db import models
# ----- HOTEL CRUD -----
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotels/add_hotel.html', {'form': form})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = hotel.reviews.all()
    avg = reviews.aggregateAvg = reviews.aggregate(models.Avg('rating'))['rating__avg']
    average_rating = round(avg, 1) if avg else "Reyting yo‘q"
    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'reviews': reviews,
        'average_rating': average_rating
    })

# ----- ROOM CRUD -----
def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()
    return render(request, 'hotels/room_list.html', {'hotel': hotel, 'rooms': rooms})

@login_required
def add_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('room_list', hotel_id=hotel.id)
    else:
        form = RoomForm()
    return render(request, 'hotels/add_room.html', {'form': form, 'hotel': hotel})

# ----- BOOKING -----
@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            room.is_available = False
            room.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'hotels/book_room.html', {'form': form, 'room': room})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})

# ----- ADMIN BOOKING MANAGEMENT -----
@staff_member_required
def all_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'hotels/all_bookings.html', {'bookings': bookings})

@staff_member_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_confirmed = True
    booking.save()
    return redirect('all_bookings')

# ----- PAYMENT & RECEIPT -----
@login_required
def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, is_confirmed=True)
    nights = (booking.check_out - booking.check_in).days
    amount = booking.room.price_per_night * nights
    if hasattr(booking, 'payment'):
        return redirect('view_receipt', payment_id=booking.payment.id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = amount
            payment.transaction_id = f'TRN{timezone.now().strftime("%Y%m%d%H%M%S")}'
            payment.save()
            return redirect('view_receipt', payment_id=payment.id)
    else:
        form = PaymentForm(initial={'amount': amount})
    return render(request, 'hotels/make_payment.html', {'form': form, 'booking': booking})

@login_required
def view_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, booking__user=request.user)
    return render(request, 'hotels/receipt.html', {'payment': payment})

@login_required
def download_receipt_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, booking__user=request.user)
    context = {'payment': payment}
    return render_to_pdf('hotels/receipt_pdf.html', context)

# ----- REVIEW -----
@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    has_booking = Booking.objects.filter(user=request.user, room__hotel=hotel, is_confirmed=True).exists()
    if not has_booking:
        return HttpResponseForbidden("Siz bu mehmonxonani baholay olmaysiz. Avva mehmonxonada yashab ko'ring!")
    if Review.objects.filter(user=request.user, hotel=hotel).exists():
        return HttpResponseForbidden("Siz allaqachon baho bergansiz.")
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.hotel = hotel
            review.save()
            return redirect('hotel_detail', hotel_id=hotel.id)
    else:
        form = ReviewForm()
    return render(request, 'hotels/add_review.html', {'form': form, 'hotel': hotel})


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Avtomatik login qiladi
            return redirect('hotel_list')  # Bosh sahifaga yo‘naltiramiz
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('hotel_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('hotel_list')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')
