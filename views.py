from django.shortcuts import redirect,render
#from django.http import HttpResponse now we are using class based view
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView #formview for user registration
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

#there is no built in view of user registration we build it using form view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class RegisterPage(FormView):
     template_name = 'baseapp/register.html'
     form_class = UserCreationForm
     redirect_authenticated_user = True
     success_url = reverse_lazy('tasks')
#now we have to redirect the user once the registration form submited
#for this we will define a function for this

     def form_valid(self, form):
          user=form.save()
          if user is not None:
               login(self.request,user)
          return super(RegisterPage,self).form_valid(form)
     #this is for what if i am logged in and i try to redirect to login page then it will restrict
     #so i need to log out first then i can redirect to login page
     def get(self,*args,**kwargs):
          if self.request.user.is_authenticated:
               return redirect('tasks')
          return super(RegisterPage,self).get(*args,**kwargs)

class CustomLoginView(LoginView):
     template_name = 'login.html'
     fields='__all__'
#go in django documentation, redirect_authenticated_user=False so we need to set it
     redirect_authenticated_user = True

     def get_success_url(self):
          return reverse_lazy('tasks')






# Create your views here.
#we ues LoginRequiredMixin before ListView bcoz we want to restrict the listview to login
#so after runserver we could see tasklist or itemlsts there but now we cant see tasklst there
# we have to first login then only we can see the listiew
#so this is the magic of LoginRedirectMixin

#do same for other views excluding loginview and logout views



#if we login with different user still it will restrict the tasklist and otherviews but it will show
#task list created by another user. so for this problem we will use get_context_data function


class TaskList(LoginRequiredMixin,ListView):
     model = Task
     context_object_name='tasks' #dont write rong spell of context
#by default the ListView looks for a template with prefix of model name(task)and suffix of __list.html if not
#..set the(task__list.html)This can e overriden by setting 'template_name' attribute
#there are so any methods of creating template but i am going to create template in app-baseap
#so i made a folder named"template" in baseapp and again i created another folder for template in "template" follder
#called as "baseapp" folder.and inside this folder i am going to put templates require

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['tasks']=context['tasks'].filter(user=self.request.user)
          context['count'] = context['tasks'].filter(complete=False).count()
          return context



class TaskDetail(LoginRequiredMixin,DetailView):
     model = Task #now this will look for template wih prefix "model name" ie. "task" and "view nae" ie. "detail"-->task_detail.html
     context_object_name = 'task'
     #it looks for task_detail.html but if i want to set the temlate name as task only then i have to set the
     #template_name='base/task.html'





class TaskCreate(LoginRequiredMixin,CreateView):
     model = Task
     #fields = ['title','description' etc..]
     #instead we wrote
     fields = ['title','description','complete']#'__all__'
     success_url = reverse_lazy('tasks')#success url means after creating and submiting task it brings us to viwes clas
     #whre the name is 'tasks' in urls.py of base class
     #this view looks for template with prefix "form"

     #when i tried different users login and after login successfully.,
     #when i tried to add task (new task) then in users i see all users in scoll bar
     #why?i have already login with username -"kanade" then why should i see another user in list while creating new task?
     #for that, form validation which is built in by django is used, Lets see!!

     def form_invalid(self, form):
          form.instance.user=self.request.user
          return super(TaskCreate,self).form_valid(form)
     #still things not worke so go to fileds and intsead of __all__ write list of fields there

class TaskUpdate(LoginRequiredMixin,UpdateView):
     model = Task
     fields = ['title','description','complete']#'__all__'
     success_url = reverse_lazy('tasks')
class TaskDelete(LoginRequiredMixin,DeleteView):
     model = Task
     context_object_name = 'task'
     success_url = reverse_lazy('tasks')

