from django.contrib import admin
from django.urls import path,include
from Platform import views
from Users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Platform.urls')), # Main Execution apps urls
    path('participant/', include('Users.urls')),
    path('programming/',include('Programming.urls')),
    path('adminsite/',include('adminsite.urls')),
]


