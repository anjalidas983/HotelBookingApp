from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
