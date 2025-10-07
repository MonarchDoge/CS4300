from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, IntegrityError
from django.contrib import messages
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('release_date')
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.select_related('movie').all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def book(self, request, pk=None):
         # Make booking atomic to avoid race conditions (two users booking same seat)
        try:
            with transaction.atomic():
                seat = Seat.objects.select_for_update().select_related('movie').get(pk=pk)
                if seat.is_booked:
                    return Response({'detail': 'Seat already booked.'}, status=status.HTTP_400_BAD_REQUEST)
                # Ensure seat belongs to requested movie if movie supplied
                movie_id = request.data.get('movie')
                if movie_id and str(seat.movie_id) != str(movie_id):
                    return Response({'detail': 'Seat does not belong to that movie.'}, status=status.HTTP_400_BAD_REQUEST)
                # Create booking (user may be anonymous)
                booking_user = request.user if request.user.is_authenticated else None
                try:
                    booking = Booking.objects.create(movie=seat.movie, seat=seat, user=booking_user)
                except IntegrityError:
                    return Response({'detail': 'Could not create booking (possible race condition).'}, status=status.HTTP_400_BAD_REQUEST)
                seat.is_booked = True
                seat.save()
        except Seat.DoesNotExist:
            return Response({'detail': 'Seat not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Without authentication, show all bookings. If auth is enabled later,
        # this can be scoped to the requesting user.
        return Booking.objects.select_related('movie', 'seat').order_by('-booking_date')

    def perform_create(self, serializer):
        seat = serializer.validated_data['seat']
        if seat.is_booked:
            raise serializers.ValidationError("Seat already booked")
        # Save user as None for anonymous requests
        user = self.request.user if getattr(self.request, 'user', None) and self.request.user.is_authenticated else None
        serializer.save(user=user)
        seat.is_booked = True
        seat.save()

# Is used to render the movie_list.html page when the app button is selected in devedu

def movie_list_view(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


# Couldn't really figure out authentication all that well so I used AI to walk
# me through it 
def seat_booking_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.filter(movie=movie).order_by('seat_number')
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        if not seat_id:
            messages.error(request, 'No seat selected.')
            return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})
        try:
            with transaction.atomic():
                seat = Seat.objects.select_for_update().get(pk=seat_id, movie=movie)
                if seat.is_booked:
                    messages.error(request, 'Seat already booked.')
                    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})
                booking_user = request.user if request.user.is_authenticated else None
                try:
                    Booking.objects.create(movie=movie, seat=seat, user=booking_user)
                except IntegrityError:
                    messages.error(request, 'Could not create booking (please try again).')
                    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})
                seat.is_booked = True
                seat.save()
        except Seat.DoesNotExist:
            messages.error(request, 'Seat not found.')
            return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})
        messages.success(request, 'Booking successful.')
        return redirect('booking_history')
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

def booking_history_view(request):
    # Show all bookings (no authentication required for this homework)
    bookings = Booking.objects.select_related('movie', 'seat').order_by('-booking_date')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})