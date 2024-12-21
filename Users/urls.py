from django.contrib import admin
from django.urls import path
from Users.views import profile,ml_contest_home,ml_submissions,file_Submit,ml_leaderboard,editUserInfo


urlpatterns = [
    path('', profile , name="profile"),
    path('image-changed',editUserInfo,name="editUserInfo"),
    path('ml-contest-home', ml_contest_home , name="ml_contest_home"),
    path('ml-file-submissions', ml_submissions , name="ml_submissions"),
    path('ml-submitted-file', file_Submit, name="file_Submit"),
    path('ml-leaderboard/<str:contest_id>', ml_leaderboard, name="ml_leaderboard")

]


