from django.shortcuts import render
from .models import Hotel,Room
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
    # import pdb;
    # pdb.set_trace()
    location = request.GET.get('location')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    travellers = request.GET.get('travellers')
    rooms_by_location = Room.objects.filter(place__name__icontains=location)


    return render(request,'hotels-available.html',{'hotels_by_location':hotels_by_location})













