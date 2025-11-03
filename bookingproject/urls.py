from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # add this
from django.shortcuts import render


def home(request):
    return render (request,'login.html')
#def register(request):
 #   return render (request,'register.html')

urlpatterns = [
    path('', home, name='home'),  # 👈 homepage route
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    
]
