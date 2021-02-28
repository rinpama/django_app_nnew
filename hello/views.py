from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Friend
from .forms import FriendForm
from django.db.models import Count,Sum,Avg,Min,Max
from django.core.paginator import Paginator

def index(request,num=1):
    data=Friend.objects.all()
    # re1=Friend.objects.aggregate(Count('age'))
    # re2=Friend.objects.aggregate(Sum('age'))
    # re3=Friend.objects.aggregate(Avg('age'))
    # re4=Friend.objects.aggregate(Min('age'))
    # re5=Friend.objects.aggregate(Max('age'))
    # msg= 'count:'+ str(re1['age__count'])\
    #     + '<br>Sum:'+ str(re2['age__sum'])\
    #         + '<br>Average:'+ str(re3['age__avg'])\
    #             + '<br>Min:'+ str(re4['age__min'])\
    #                 + '<br>Max:'+ str(re5['age__max'])


    # params={
    #     'title':'Hello',
    #     'message': msg,
    #     'data':data,
    # }
    page=Paginator(data,3)
    params={
        'title':'Hello',
        'message':'',
        'data':page.get_page(num)
    }
    return render(request,'hello/index.html',params)

#create model
def create(request):
    if (request.method == 'POST'):
        obj=Friend()
        friend=FriendForm(request.POST,instance=obj)
        friend.save()
        return redirect(to='/hello')

    params={
        'titile':'Hello',
        'form':FriendForm(),
        }      
    return render(request,'hello/create.html',params)

def edit(request,num):
    obj=Friend.objects.get(id=num)
    if (request.method== 'POST'):
        friend= FriendForm(request.POST,instance=obj)
        friend.save()
        return redirect(to='/hello')
    params={
        'title':'Hello',
        'id':num,
        'form':FriendForm(instance=obj),
    }
    return render(request,'hello/edit.html',params)

def delete(request,num):
    friend=Friend.objects.get(id=num)
    if (request.method=='POST'):
        friend.delete()
        return redirect(to='/hello')
    params={
        'title':'Hello',
        'id':num,
        'obj':friend,

    }
    return render(request,'hello/delete.html',params)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import FindForm
from django.db.models import Q
from .forms import CheckForm
from .models import Message
from .forms import MessageForm

class FriendList(ListView):
    model= Friend

class FriendDetail(DetailView):
    model= Friend

# def find(request):
#     if (request.method== 'POST'):
#         msg= 'search result:'
#         form =FindForm(request.POST)
#         find= request.POST['find']
#         list=find.split()
#         data=Friend.objects.all()[int(list[0]):int(list[1])]
#     else:
#         msg= 'search words...'
#         form= FindForm()
#         data= Friend.objects.all()
#     params={
#         'title':'Hello',
#         'message':msg,
#         'form':form,
#         'data':data,

#     }
#     return render(request,'hello/find.html',params)
def find(request):
    if (request.method=='POST'):
        msg=request.POST['find']
        form=FindForm(request.POST)
        sql='select * from hello_friend' 
        if (msg !=''):
            sql +=' where ' + msg
        data= Friend.objects.raw(sql)
        mag= sql
    else:
        msg= 'search words..'
        form= FindForm()
        data= Friend.objects.all()
    params= {
        'title':'Hello',
        'message':msg,
        'form':form,
        'data':data,

    }
    return render(request,'hello/find.html',params)



# def check(request):
#     params={
#         'title':'Hello',
#         'message':'check validation.',
#         'form':CheckForm(),

#     }
#     if (request.method== 'POST'):
#         form=CheckForm(request.POST)
#         params['form']= form
#         if (form.is_valid()):
#             params['message']='OK!'
#         else:
#             params['message']='no good'
#     return render(request,'hello/check.html',params)

def check(request):
    params={
        'title':'Hello',
        'message':'check validation.',
        'form':FriendForm(),

    }
    if (request.method== 'POST'):
        form=FriendForm(request.POST)
        params['form']= form
        if (form.is_valid()):
            params['message']='OK!'
        else:
            params['message']='no good'
    return render(request,'hello/check.html',params)

def message(request,page=1):
    if (request.method== 'POST'):
        obj=Message()
        form= MessageForm(request.POST,instance=obj)
        form.save
    data= Message.objects.all().reverse()
    paginator= Paginator(data,2)
    params={
        'title':'Message',
        'form':MessageForm(),
        'data':paginator.get_page(page),
        
    }
    return render(request,'hello/message.html',params)
