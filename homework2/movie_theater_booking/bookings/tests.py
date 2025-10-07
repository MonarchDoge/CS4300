from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Movie, Seat

User = get_user_model()

# Tests if the booking API correctly functions
# Includes user and movie creation, listing the movies, and booking seats.
class BookingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'pass')
        self.movie = Movie.objects.create(title='M', description='d', release_date='2025-01-01', duration=120)
        self.seat = Seat.objects.create(movie=self.movie, seat_number='A1')

    def test_list_movies(self):
        resp = self.client.get('/api/movies/')
        self.assertEqual(resp.status_code, 200)

    def test_book_seat(self):
        self.client.login(username='test', password='pass')
        resp = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp.status_code, 201)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)


    def test_anonymous_book_seat(self):
        # Ensure anonymous users can book (user set to null)
        resp = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp.status_code, 201)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_anonymous_web_book_seat(self):
        # Test posting to the site booking view as anonymous user
        resp = self.client.post(f'/movies/{self.movie.id}/book/', {'seat_id': self.seat.id})
        # Expect a redirect to booking history on success
        self.assertIn(resp.status_code, (302, 200))
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)


    def test_movie_seat_listing(self):
        # Movie list page should render and include the movie title
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.movie.title.encode(), resp.content)

    def test_double_book_api(self):
        # First booking should succeed; second should fail
        resp1 = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp2.status_code, 400)

    def test_double_book_web(self):
        # Web booking twice should show an error for the second attempt
        resp1 = self.client.post(f'/movies/{self.movie.id}/book/', {'seat_id': self.seat.id})
        self.assertIn(resp1.status_code, (302, 200))
        resp2 = self.client.post(f'/movies/{self.movie.id}/book/', {'seat_id': self.seat.id})
        # The view returns 200 with an error message in the page
        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b'Seat already booked', resp2.content)

    def test_book_nonexistent_seat(self):
        resp = self.client.post(f'/api/seats/9999/book/', {'movie': self.movie.id})
        self.assertEqual(resp.status_code, 404)

    def test_web_missing_seat_param(self):
        # Posting without seat_id should return the form with an error message
        resp = self.client.post(f'/movies/{self.movie.id}/book/', {})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'No seat selected', resp.content)

    def test_booking_history_list(self):
        # Create two bookings (one anonymous, one authenticated)
        self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        # Create new seat for second booking
        seat2 = Seat.objects.create(movie=self.movie, seat_number='A2')
        self.client.login(username='test', password='pass')
        self.client.post(f'/api/seats/{seat2.id}/book/', {'movie': self.movie.id})
        # Booking history page should list both bookings
        resp = self.client.get('/history/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'A1', resp.content)
        self.assertIn(b'A2', resp.content)

    def test_concurrent_like_booking(self):
        # Simulate quick sequential attempts: first succeeds, second fails
        resp1 = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post(f'/api/seats/{self.seat.id}/book/', {'movie': self.movie.id})
        self.assertEqual(resp2.status_code, 400)