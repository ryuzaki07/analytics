from django.urls import path

from django.urls import include


from . import views

urlpatterns = [
    path('', views.query, name='query'),
    path('datesvssessions/',views.DateVsSessionsFormView,name='datesvssessions'),
    path('datesvssessionsview/',views.DateVsSessionsView,name='datesvssessionsview'),
     path('usertype/',views.UsertypeFormView,name='usertypeformview'),
     path('usertypeview/',views.UsertypeView,name='usertypeview'),
]




