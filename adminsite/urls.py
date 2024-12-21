from django.contrib import admin
from django.urls import path
from adminsite.views import admin_dashboard,admin_ml_contest,admin_ml_contest_confirmation,admin_ml_contest_remove_confirmation,admin_ml_contest_details,userManagement,give_org_acces,remove_org_access,organizational_profile,admin_user_profile,admin_programming_contest_list,admin_programming_contest_confirmation,admin_programming_contest_remove_confirmation, admin_programming_contest_details


urlpatterns = [
    path('', admin_dashboard, name="admin_dashboard"),
    path('ml-contest-list',admin_ml_contest, name="admin_ml_contest_list"),
    path('ml-contest-list-approve',admin_ml_contest_confirmation, name="admin_ml_contest_confirmation"),
    path('ml-contest-details',admin_ml_contest_details, name = "admin_ml_contest_details"),
    path('ml-contest-list-pending', admin_ml_contest_remove_confirmation, name="admin_ml_contest_remove_confirmation"),
    path('user-management', userManagement , name="userManagement"),
    path('give-access', give_org_acces, name="give_org_access"),
    path('remove-access', remove_org_access, name="remove_org_access"),
    path('organizational-profile', organizational_profile, name = "organizational_profile"),
    path('user-profile',admin_user_profile, name="admin_user_profile"),
    path('programming-contest-list',admin_programming_contest_list, name="admin_programming_Contest_List"),
    path('programming-contest-list-approve',admin_programming_contest_confirmation, name="admin_programming_contest_confirmation"),
    path('programming-contest-details',admin_programming_contest_details, name = "admin_programming_contest_details"),
    path('programming-contest-list-pending', admin_programming_contest_remove_confirmation, name="admin_programming_contest_remove_confirmation"),

]

