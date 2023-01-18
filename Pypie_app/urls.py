from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index),
    path('register' , views.user_register),
    path('login' , views.user_login) , 
    path('dashboard', views.success_login),
    path('dashboard/addpie' , views.add_pie),
    path ('logout' , views.user_logout),
    path('dashboard/<int:id>/delete', views.delete_Pie),
    path ('dashboard/<int:pie_id>/edit' , views.edit_pie),
    path ('dashboard/<int:pie_id>/edit/update' , views.update_pie),
    path('pies' , views.view_all_pie),
    path('show/<int:pie_id>/like',views.add_vote), 
    path('show/<int:pie_id>' , views.show_pie) ,
    path('show/<int:pie_id>/dislike',views.remove_vote), 
]