"""
URL configuration for lead_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("index/",views.IndexView.as_view(),name="index"),
    
    path("signup/",views.SignupView.as_view(),name="signup"),

    path("signin/",views.SinginView.as_view(),name="signin"),
    
    path('singout/',views.SignoutView.as_view(),name="signout"),

    path("lead/add/",views.LeadAddView.as_view(),name="lead_add"),

    path("task/add/",views.TaskAddView.as_view(),name="task_add"),

    path("lead/list/",views.LeadListView.as_view(),name="lead_list"),

    path("task/list/",views.TaskListView.as_view(),name="task_list"),

    path("lead/<int:pk>/detail/",views.LeadDetailView.as_view(),name="lead_detail"),

    path("lead/<int:pk>/update",views.LeadUpdateView.as_view(),name="lead_update"),

    path("lead/<int:pk>/delete/",views.LeadDeleteView.as_view(),name="lead_delete"),

    path("lead/add/file/",views.LeadImportView.as_view(),name="lead_file"),

    path("notification/",views.NotificationAddView.as_view(),name="notification"),
    path("notification/list/",views.NotificationListView.as_view(),name="notification_list")

]
