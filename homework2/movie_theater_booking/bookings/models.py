from django.conf import settings
from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    movie = models.ForeignKey(Movie, related_name='seats', on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seat_number', 'movie')

    def __str__(self):
        return f"{self.movie.title} - {self.seat_number}"

class Booking(models.Model):
    movie = models.ForeignKey(Movie, related_name='bookings', on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookings', on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seat', 'movie')

    def __str__(self):
        user_str = str(self.user) if self.user else 'Anonymous'
        return f"{user_str} booked {self.seat} for {self.movie}"