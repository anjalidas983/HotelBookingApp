from django.urls import path
from . import views
app_name = "booking"

urlpatterns = [
    path("", views.home, name='home'),
    path('hotel-search/',views.hotel_search,name='hotel-search'),
    path('find-hotel/',views.find_hotel,name='find-hotel')
]