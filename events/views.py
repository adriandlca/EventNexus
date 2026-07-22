from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def detail_page(request,event_id):
    return render(request,'events/detail.html',{'event_id':event_id})

@login_required(login_url='core:login_page')
def create_events_page(request):
    return render(request,'events/evento_form.html')
