import profile
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import FormRegistrazione
from app.models import Profile
# Create your views here.

def registrazione_view(request):
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = User.objects.create_user(username=username, email=email, password=password)
            new_user = Profile(user=user)
            new_user.btc_original = new_user.btc_wallet
            new_user.save()
            autentificazione_user = authenticate(username=username, passowrd=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else: 
        form = FormRegistrazione()
    context = {'form': form}
    return render (request, "accounts/registrazione.html", context)