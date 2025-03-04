from django.urls import path
from.import views

urlpatterns =[
    path('',views.index,name='index'),
    path('setting',views.setting,name='setting'),
    path('upload',views.upload,name='upload'),
    path('follow',views.follow,name='follow'),
    path('like-post',views.like_post,name='like-post'),
    path('signup/',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('search',views.search,name='search')
]