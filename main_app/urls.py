from django.urls import path

from main_app import views

urlpatterns = [
    path('register/', views.register,name="register"),
    path('login/', views.loginpage,name="loginpage"),
    path('profile/', views.profile_page,name="profile_page"),
    path('logout/', views.logout_page,name="logoutpage"),
    path('jobpost/', views.create_jobpost,name="jobpost"),
    path('', views.job_list,name="joblist"),
]
