from django.shortcuts import render,redirect
#from django.http import HttpResponse
# Create your views here.
from .models import *
#we are importing forms.py file for each task we can use so,
from .forms import *





def index(request):
    tasks=Task.objects.all()
    form=TaskForm()

    if request.method=='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context={'tasks':tasks,'form':form}
    return render(request,'todoapp1/list.html',context)

def update_task(request,pk):
    task = Task.objects.get(id=pk)
    form=TaskForm(instance=task)

    if request.method=='POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'todoapp1/update.html',context)


def delete_task(request,pk):
    item=Task.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('/')
    context={'item':item}

    return render(request,'todoapp1/delete_task.html',context)
