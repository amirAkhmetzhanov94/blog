from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.generic import View


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        return render(request, "registration/login.html", {"has_error": True})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("index")
