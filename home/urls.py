from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('',views.home,name='home'),
    path('post',views.post,name='post'),
    path('blogpost/<str:slug>',views.blogpost,name='blogpost'),
    path('search',views.search,name='search'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('editor',views.editor,name='editor'),
    path('comment',views.comment,name='comment'),

]
