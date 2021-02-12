from django.shortcuts import render
import datetime

def home(request):
    year = datetime.datetime.now().year
    return render(request,"home.html",{'year':year})
