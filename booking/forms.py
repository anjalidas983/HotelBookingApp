from . models import Bookings,Reviews
from django import forms

# class BookingsForm(forms.Form):
#     name =forms.CharField(label='Full Name')
#     hotel=forms.CharField(label='Hotel Name')
#     room =forms.CharField(label='Room')
#     num_room=forms.IntegerField(label='Number of Rooms')
#     check_in=forms.DateField(label="Check in Date")
#     check_out=forms.DateField(label='Check out Date')
class BookingsForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields ='__all__'


class ReviewsForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields = '__all__'