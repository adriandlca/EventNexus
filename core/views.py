from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

# Create your views here.
def home_page(request):
    return render(request,'index.html')

def login_page(request):
    return render(request,'auth/login.html')

def register_page(request):
    return render(request,'auth/register.html')

@require_POST
def logout_page(request):
    logout(request)
    return redirect('core:login_page')
