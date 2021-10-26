"""issue_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import accounts.views
from webapp import views as webview

urlpatterns = [
    path('accounts/login/', accounts.views.LoginView.as_view(), name='login'),
    path('accounts/logout/', accounts.views.LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('', webview.IndexView.as_view(), name='index'),
    path('issue/<int:issue_pk>/', webview.IssueView.as_view(), name='issue_detail'),
    path('issue/add/', webview.AddIssue.as_view(), name="issue_add"),
    path('issue/edit/<int:pk>/', webview.UpdateIssue.as_view(), name="issue_update"),
    path('issue/delete/<int:pk>', webview.DeleteIssue.as_view(), name="issue_delete"),
    path('projects-list/', webview.ProjectListView.as_view(), name='project_list'),
    path('detailed/<int:pk>', webview.ProjectDetailedView.as_view(), name='project_detail'),
    path('project/add', webview.ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/issue/add', webview.ProjectCreateIssue.as_view(), name='project_add_issue')
]
