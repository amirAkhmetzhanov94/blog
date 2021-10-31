from django.urls import path
from webapp import views as webview
from accounts.views import RemoveFromProjectView, AddToProjectView

app_name = "webapp"

urlpatterns = [
    path('', webview.IndexView.as_view(), name='index'),
    path('issue/<int:issue_pk>/', webview.IssueView.as_view(), name='issue_detail'),
    path('issue/add/', webview.AddIssue.as_view(), name="issue_add"),
    path('issue/edit/<int:pk>/', webview.UpdateIssue.as_view(), name="issue_update"),
    path('issue/delete/<int:pk>', webview.DeleteIssue.as_view(), name="issue_delete"),
    path('projects-list/', webview.ProjectListView.as_view(), name='project_list'),
    path('detailed/<int:pk>', webview.ProjectDetailedView.as_view(), name='project_detail'),
    path('project/add', webview.ProjectCreateView.as_view(), name='project_add'),
    path('project/delete/<int:pk>', webview.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/update/<int:pk>', webview.ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/issue/add', webview.ProjectCreateIssue.as_view(), name='project_add_issue'),
    path('project/<int:project_pk>/account/remove/',
         RemoveFromProjectView.as_view(), name='project_remove_user'),
    path('project/<int:project_pk>/account/add/', AddToProjectView.as_view(), name='project_add_user')
]
