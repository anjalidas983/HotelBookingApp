from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, UserAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def registration_view(request):
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking:home')

    else:
        form = UserForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):

    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('booking:home')       
        else:
            form = UserAuthenticationForm()
            messages.error(request,'Invalid username or password')  

    else:
        form = UserAuthenticationForm()         
    return render(request,'login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    return redirect('booking:home')