from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='places/')
    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    owner = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    facilities = models.ManyToManyField(Facility)
    hotelimage = models.ImageField(upload_to='hotels/',null=True)
    def __str__(self):
        return self.hotel_name

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='stay')
    image = ProcessedImageField(upload_to='hotels/', format='JPEG', options={'quality': 90})




class RoomCategory(models.Model):
    category_type = models.CharField(max_length=100)
    is_ac = models.BooleanField()
    num_people = models.IntegerField()
    def __str__(self):
        return self.category_type



class Room(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    total_room = models.IntegerField()
    room_rate = models.IntegerField()
    image = models.ImageField(upload_to='rooms/')







class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rooms_booked = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review = models.TextField(max_length=100)
    rating = models.IntegerField()
    def __str__(self):
        return f"{self.rating}"






