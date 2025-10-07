from rest_framework import serializers
from .models import Movie, Seat, Booking

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked', 'movie']

class MovieSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration', 'seats']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'movie', 'seat', 'user', 'booking_date']
        read_only_fields = ['user', 'booking_date']

    def get_user(self, obj):
        return str(obj.user) if obj.user else None