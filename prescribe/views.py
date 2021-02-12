from django.shortcuts import render
import datetime

def prescribe(request):
    year = datetime.datetime.now().year
    return render(request,"prescribe.html",{'year':year})
