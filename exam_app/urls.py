from django.urls import path
from . import views
urlpatterns = [
    path("",views.index),
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
    path("dashboard", views.dashboard),
    path("wishes/new",views.new_wish),
    path("create_wish",views.create_wish),
    # path("trips/<int:id>",views.read_trip),
    path("wishes/edit/<int:id>",views.edit),
    path("update/<int:id>",views.update),
    path("wishes/delete/<int:id>",views.delete),
    path("wishes/like/<int:id>",views.like),
    path("wishes/stats",views.stats),
    path("granted/<int:id>",views.granted)
    
]