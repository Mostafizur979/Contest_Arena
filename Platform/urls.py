from django.contrib import admin
from django.urls import path
from Platform.views import Landing_Page,Host_ML_Contest,host_contest_list,authentication,ml_contest_edit,ml_contest_edited_info,register,signin,verification,ml_contest_registration, ml_contest_registration_successfull,ml_contest_add_participant,ml_contest_registration_approved,oraganizational_dashboard,mlContestDetails,logout_view


urlpatterns = [
    path('', Landing_Page , name="Landing_Page"),
    path('create-new-contest/', Host_ML_Contest, name="Host_Contest"),
    path('host-contest-list/', host_contest_list, name="host_contest_list"),
    path('ml-contest-information-edit/', ml_contest_edit, name="ml_contest_edit"),
    path('ml-contest-information-edited/', ml_contest_edited_info, name="ml_contest_edited_info"),
    path('ml-contest-details/', mlContestDetails, name="mlContestDetails"),
    path('authentication', authentication, name="authentication"),
    path('signin/', signin, name="signin"),
    path('register/', register, name="register"),
    path('verification/', verification, name="verification"),
    path('ml-contest-registration-form/',ml_contest_registration, name="ml_contest_registration"),
    path('ml-contest-registration-form-sent/', ml_contest_registration_successfull, name="ml_contest_registration_successfull"),
    path('ml-contest-add-team/',ml_contest_add_participant, name="ml_contest_add_participant"),
    path('ml-contest-approved-team/',ml_contest_registration_approved, name="ml_contest_registration_approved"),
    path('organizational-dashboard/',oraganizational_dashboard, name="oraganizational_dashboard"),
    path('logout',logout_view,name="logout"),
]


