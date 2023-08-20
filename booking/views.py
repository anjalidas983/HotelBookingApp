from django.shortcuts import render
from .models import Hotel,Room,Bookings
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,"home.html")

def hotel_search(request):
    location = request.GET.get('search')
    hotels = []

    if location:
        hotels = Hotel.objects.filter(place__name__icontains = location)

    total_hotels = len(hotels)
    context = {
        'location':location,
         'hotels':hotels,
        'total_hotel':total_hotels
    }
    return render(request,'hotel-search.html',context)
def find_hotel(request):
    import pdb;
    pdb.set_trace()
    location = request.GET.get('location')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    travellers = request.GET.get('travellers')
    rooms_by_location = Room.objects.filter(place__name__icontains=location,\
                                            room_category__num_people=travellers)
    hotel_names = rooms_by_location.values_list('hotel__hotel_name',flat=True)
    room_type = rooms_by_location.values_list('room_category__category_type',flat=True)
    booked_rooms_same_type = Bookings.objects.filter(room__place__name = location,\
                           hotel__hotel_name__in=hotel_names,\
                      room__room_category__category_type__in=room_type)




    return render(request,'hotels-available.html',{'rooms_by_location':rooms_by_location})













