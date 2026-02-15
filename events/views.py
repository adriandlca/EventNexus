from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request,'events/home.html')

def detail_page(request,event_id):
    return render(request,'events/detail.html',{'event_id':event_id})

def create_events_page(request):
    return render(request,'events/evento_form.html')