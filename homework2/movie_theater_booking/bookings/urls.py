from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, SeatViewSet, BookingViewSet
from . import views as web_views

router = DefaultRouter()
router.register(r'api/movies', MovieViewSet)
router.register(r'api/seats', SeatViewSet)
router.register(r'api/bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', web_views.movie_list_view, name='movie_list'),
    path('movies/<int:movie_id>/book/', web_views.seat_booking_view, name='seat_booking'),
    path('history/', web_views.booking_history_view, name='booking_history'),
    path('', include(router.urls)),
]