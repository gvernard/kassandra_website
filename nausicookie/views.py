from django.shortcuts import render
import random
import sys

def hello_nausicookie(request):
    combined = []
    rows = [1,2,3,4,5,6,7,8]
    cols = [1,2,3,4,5,6]
    for i in rows:
        for j in cols:
            combined.append(str(i)+str(j))
    random.shuffle(combined)
    
    img_ids = []
    img_src = []
    for item in combined:
        i = item[0:1]
        j = item[1:2]
        img_ids.append( i+j )
        img_src.append( 'image_'+i+'_'+j+'.jpeg' )
    
    mylist = zip(img_ids,img_src)
    context = {
        'indices': mylist,
    }
    return render(request,'nausicookie.html',context)
