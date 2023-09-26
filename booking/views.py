from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Hotel,Room,Bookings,HotelImage,Place,Reviews
from collections import defaultdict
from datetime import datetime
from django.db.models import Q
from . forms import BookingsForm,ReviewsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import UserWallet
# Create your views here.

def home(request):
    places=Place.objects.all()
    return render(request,"home.html",{'places':places})

def hotel_search(request):
    if request.method == "GET":
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
    
def hotel_search_view(request,id):
    hotel=Hotel.objects.get(id=id)
    hotelimages=HotelImage.objects.filter(hotel__id=id)
    return render(request,'hotels.html',{'hotel':hotel,'hotelimages':hotelimages})

def find_hotel_2(request):
    if not request.user.is_authenticated:
        return redirect('account:user_login')
    else:
        location = request.GET.get('location')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        travellers = request.GET.get('travellers')
        input_checkin = datetime.strptime(checkin, "%Y-%m-%d")
        input_checkout = datetime.strptime(checkout, "%Y-%m-%d")
        request.session['check_in'] = input_checkin.isoformat()
        request.session['check_out'] = input_checkout.isoformat()
        room_cat = ''
        if travellers == '1':
            room_cat = 'Single Room'
        elif travellers == '2':
            room_cat = 'Double Room'
        elif travellers == '3':
            room_cat = 'Triple Room'
        else:
            room_cat = 'Family Room'
        rooms_in_location = Room.objects.filter(place__name__icontains=location,room_category__category_type=room_cat)\
            .select_related('place', 'hotel', 'room_category')
        
        # room_category__num_people=travellers
        # finding conflicting bookings in a place for the input date range.
        bookings_date_loc = Bookings.objects.filter((Q(check_out__gte=input_checkin) &
            Q(check_in__lt=input_checkout)), room__place__name__icontains=location,room__room_category__category_type=room_cat)\
            .select_related('hotel', 'room')
        # print(bookings_date_loc.all())
        rooms_bookings = []
        for room in rooms_in_location:
            '''
            iterating through each room in the location
            '''
            
            combined_details_per_room = {
                "room_id":room.id,
                "hotel_id":room.hotel.id,
                "hotel_name": room.hotel.hotel_name,
                "hotel_description":room.hotel.description,
                "facilities":room.hotel.facilities.prefetch_related(),
                "images":room.hotel.hotelimage,
                "room_category": {
                    "type": room.room_category.category_type,
                    "num_adults": room.room_category.num_people,
                    "air_conditioned": room.room_category.is_ac
                },
                "total_rooms": room.total_room,
                "available_rooms": room.total_room,
                "rate":room.room_rate,
                "room_image":room.image
            }
            total_customer_bookings = 0
            for booking in bookings_date_loc:
                '''
                Iterate through conflicting/lapsing bookings made by all users
                '''
                # if room.id == booking.room.id and room.hotel.id == booking.hotel.id:
                if room.hotel.id == booking.hotel.id:
                    # conflicting bookings for input date identified
                    total_customer_bookings += booking.rooms_booked
            # combined_details_per_room["available_rooms"] = max(0, (room.total_room -
            #     total_customer_bookings))
            combined_details_per_room["available_rooms"] =(room.total_room)-(total_customer_bookings)
            rooms_bookings.append(combined_details_per_room)
    
    return render(request,'hotels-available.html',{'rooms_available':rooms_bookings})




def hotel_detail_view(request,id,type):
    rooms=Room.objects.filter(hotel__id=id,room_category__category_type=type).select_related('hotel')
    hotelimages=HotelImage.objects.filter(hotel__id=id)
    reviews=Reviews.objects.filter(hotel__id=id)
    user = request.user if request.user.is_authenticated else None
    
    if request.method=="POST":
        form=ReviewsForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReviewsForm() 
            messages.success(request, 'Review submitted successfully')
        else:
            messages.error(request,'Invalid')
    else:
        initial_data ={
        'user':request.user,
        'hotel':rooms[0].hotel,
        'review':'',
        'rating':'',
    }

        form=ReviewsForm(initial=initial_data)
    return render(request,'single-hotel-view.html',{'rooms':rooms,'hotelimages':hotelimages,'form':form,'reviews':reviews})








def hotel_booking(request,id,type):
    check_in=request.session.get('check_in')
    check_out=request.session.get('check_out')
    rooms = Room.objects.filter(hotel__id=id,room_category__num_people=type).select_related('hotel','room_category')
    hotel_id=[]
    room_id=[]
    data_list = []
    for room in rooms:
       h_id ={'hotel_id':room.hotel.id}     
       r_pk ={'room_id':room.id }  
       data={'hotel':room.hotel,'room':room.id}
       data_list.append(data)
       hotel_id.append(h_id)
       room_id.append(r_pk)
    hotel_data = data_list[0] if data_list else {}
    id_data = hotel_id[0] if hotel_id else {}
    roomid_data = room_id[0] if room_id else {}
    
    initial_data = {
        'user':request.user,
        'hotel':hotel_data.get('hotel',None),
        'room':hotel_data.get('room',None),
        'rooms_booked':1,
        'check_in':datetime.fromisoformat(check_in),
        'check_out':datetime.fromisoformat(check_out)
       
    }
   
    form=BookingsForm(initial=initial_data)

    # form=BookingsForm(initial=data)

    return render(request,'booking-form.html',{'form':form,'id_data':id_data,'roomid_data':roomid_data}) 

def reserve_room(request,id,pk):
    room =Room.objects.get(hotel__id=id,id=pk)
    data={'user':request.user,'hotel':room.hotel.hotel_name,'room':room.room_category.category_type}
    if request.method=="POST":
        num_rooms=request.POST['rooms_booked']
        total_rate=int(num_rooms)*room.room_rate
        form=BookingsForm(request.POST)
        if form.is_valid():
            booking=form.save()
            booking_id=booking.id
            return render(request,'payment.html',{'room':room,'room_booked':num_rooms,'total_rate':total_rate,'booking_id':booking_id})
        else:
            return render(request,'booking-form.html',{'form':form})
    else:
        form=BookingsForm(initial=data)
        # form=BookingsForm()
        return render(request,'booking-form.html',{'form':form})  
    return render(request,'booking-form.html')

def booking_payment(request):
    return render(request,'payment.html')

def payment_processing(request):
    return render(request,'hotel-booked.html')

# def payment_processing(request,id,type,b_id):
#     room=Room.objects.get(hotel__id=id,room_category__category_type=type)
#     hotel_bookings=Bookings.objects.get(id=b_id)
#     if request.method=="POST":
#         total_rate=request.POST['total']
#         room_booked = request.POST['num_room']

#         user=UserWallet.objects.get(user__id=request.user.id)
#         user.balance-=total_rate
#         user.save()
#         messages.success(request,'Room booked successfully.')
#         if user.balance-total_rate==user.balance:
#             hotel_bookings.delete()
#             messages.error(request,'Payment not completed.Booking Cancelled.')
#             return redirect('booking:home')

#     else:
#         return render(request,'payment.html',{'room':room})


    
        

def all_hotels(request):
    hotels=Hotel.objects.all()
    return render(request,'all-hotels.html',{'hotels':hotels})


def attractions(request):
    places=Place.objects.all()
    return render(request,'attractions.html',{'places':places})