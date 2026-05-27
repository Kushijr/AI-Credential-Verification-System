from django.urls import path

from . import views

urlpatterns = [

    path('', views.home),

    path(
        'approve/<int:id>/',
        views.approve_credential
    ),

    path(
        'verify/<int:id>/',
        views.verify_credential
    ),

    path(
        'reject/<int:id>/',
        views.reject_credential
    ),

]