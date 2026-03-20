from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'auth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username', request.user.username)
        request.user.bio = request.POST.get('bio', request.user.bio)
        request.user.save()
        messages.success(request, 'Profile updated.')
    return render(request, 'auth/profile.html')
