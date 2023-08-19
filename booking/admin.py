from django.contrib import admin
from . models import Place, Facility, Hotel, RoomCategory, Bookings, Room, Reviews,HotelImage
# Register your models here.
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_type','is_ac','num_people',]
class  RoomAdmin(admin.ModelAdmin):
    list_display = ['place','hotel','room_category','total_room','room_rate']
    list_filter = ('place','hotel','room_category',)
    search_fields = ('room_category__category_type',)

class BookingsAdmin(admin.ModelAdmin):
    list_display = ['user','hotel','room','rooms_booked','check_in','check_out']

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user','hotel','review','rating']
admin.site.register(Place)
admin.site.register(Facility)
admin.site.register(Hotel)
admin.site.register(RoomCategory,RoomCategoryAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Reviews,ReviewsAdmin)
admin.site.register(Bookings,BookingsAdmin)
admin.site.register(HotelImage)

