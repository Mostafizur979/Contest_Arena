from django.contrib import admin
from django.urls import path
from Programming.views import Host_Programming_Contest,Programming_contest_list,Programming_Contest_Edit,programming_contest_edited_info,programming_contest_registration,programming_contest_registration_successfull,programming_contest_add_participant,programming_contest_registration_approved,create_Problemset,programming_contest_home,contestProblems,run_code,submit_code, programming_leaderboard,programming_contest_details


urlpatterns = [
    path('', Host_Programming_Contest , name="Host_Programming_Contest"),
    path('contest-list', Programming_contest_list, name="Programming_Contest_List"),
    path('contest-info-edit', Programming_Contest_Edit, name="Programming_Contest_Edit"),
    path('contest-info-edited', programming_contest_edited_info, name="programming_contest_edited_info"),
    path('contest-info-registration', programming_contest_registration, name="programming_contest_registration"),
    path('Home', programming_contest_registration_successfull, name="programming_contest_registration_successfull"),
    path("contest-participant-request-approval",programming_contest_add_participant, name="programming_contest_add_participant"),
    path("contest-participant-request-approved",programming_contest_registration_approved, name="programming_contest_registration_approved"),
    path("create-problemset",create_Problemset,name="create_Problemset"),
    path("contest",programming_contest_home,name="programming_contest_home"),
    path("problems", contestProblems , name = "contestProblems"),
    path("problem-run", run_code, name="run_code"),
    path("problem-submitted", submit_code, name="submit_code"),
    path("leaderboard", programming_leaderboard, name="programming_leaderboard"),
    path('programming-contest-details',programming_contest_details, name="programming_contest_details"),
]


