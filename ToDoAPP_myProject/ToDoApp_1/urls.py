from django.urls import path
#we have to import views.py so that we can connect index fun here (from . means=from root)
from . import views

#now we can mention index fun of views.py in urlpatterns
urlpatterns=[
    path('',views.index,name="list") , #in path function we write('') because we want to open views.index first ie. as a HOMEPAGE
    path('update_task/<str:pk>/',views.update_task,name="update_task"),
    path('delete_task/<str:pk>/',views.delete_task,name="delete_task"),


]