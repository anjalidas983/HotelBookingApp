from django.urls import path
from . import views
app_name = "booking"

urlpatterns = [
    path("", views.home, name='home'),
    path('hotel-search/',views.hotel_search,name='hotel-search'),
    path('find-hotel/',views.find_hotel_2,name='find-hotel'),
    path('hotel-detail-view/<int:id>/<str:type>/',views.hotel_detail_view,name="detail-view"),
    path('hotel-booking/<int:id>/<int:type>/',views.hotel_booking,name='hotel_booking'),
    path('reserve-room/<int:id>/<int:pk>/',views.reserve_room,name='reserve-room'),
    path('payment/',views.booking_payment,name='payment'),
    path('booking-payment/',views.payment_processing,name='booking_payment'),
    path('hotel-details/<int:id>/',views.hotel_search_view,name='search_hotel_details'),
    path('all-hotels/',views.all_hotels,name='all-hotels'),
    path('attractions/',views.attractions,name='attractions'),
]