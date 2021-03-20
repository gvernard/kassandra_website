from django.shortcuts import render
import random

def hello_nausicookie(request):
    rows = [1,2,3,4,5,6,7,8]
    cols = [1,2,3,4,5,6]
    #random.shuffle(rows)
    #random.shuffle(cols)
    
    img_ids = []
    img_src = []
    for i in rows:
        for j in cols:
            img_ids.append( str(i)+str(j) )
            img_src.append( 'image_'+str(i)+'_'+str(j)+'.jpeg' )
    
    mylist = zip(img_ids,img_src)
    context = {
        'indices': mylist,
    }
    return render(request,'nausicookie.html',context)
