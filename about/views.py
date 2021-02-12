from django.shortcuts import render
import datetime

def about(request):
    year = datetime.datetime.now().year
    return render(request,"about.html",{'year':year})
