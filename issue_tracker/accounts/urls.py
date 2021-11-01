from django.urls import path
from accounts.views import LoginView, LogoutView, RegisterView, UserDetailView, UserListView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='list')
]
