from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # authenticate using username (Django's default)
        # if you use email for login, you must map it to username
        try:
            from django.contrib.auth.models import User
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')  # redirect after login
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'users/login.html')
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

#def register_view(request):
 #   return render(request, "users/register.html")

