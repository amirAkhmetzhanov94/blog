from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views.generic import View, CreateView, DetailView
from django.http import HttpResponseRedirect
from accounts.forms import RegistrationForm
from webapp.models import Project
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_path = request.POST.get("next")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_path:
                return HttpResponseRedirect(next_path)
            return redirect("webapp:index")
        return render(request, "registration/login.html", {"has_error": True})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("webapp:index")


class RegisterView(CreateView):
    model = User
    template_name = "registration/register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class RemoveFromProjectView(UserPassesTestMixin, View):
    template_name = 'remove.html'

    def get_object(self):
        pk = self.kwargs.get("project_pk")
        return Project.objects.get(pk=pk)

    def test_func(self):
        return self.request.user.has_perm('auth.delete_user') and self.request.user in self.get_object().users.all()

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        user_id = request.GET.get("user_id")
        project = get_object_or_404(Project, id=project_id)
        user = User.objects.get(id=user_id)
        return render(request, self.template_name, {"user": user, "project": project})

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        project = get_object_or_404(Project, id=project_id)
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        choice = request.POST.get("choice")
        if choice == "Yes":
            project.users.remove(user)
        return redirect("webapp:project_detail", pk=project.pk)


class AddToProjectView(UserPassesTestMixin, View):
    template_name = 'add.html'

    def get_object(self):
        pk = self.kwargs.get("project_pk")
        return Project.objects.get(pk=pk)

    def test_func(self):
        return self.request.user in self.get_object().users.all() and self.request.user.has_perm('auth.add_user')

    def get(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        project = get_object_or_404(Project, id=project_id)
        return render(request, self.template_name, {"project": project})

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get("project_pk")
        project = get_object_or_404(Project, id=project_id)
        user_request = request.POST.get("user_id")
        user = None
        try:
            user = User.objects.get(username=user_request)
            project.users.add(user)
            return redirect("webapp:project_detail", pk=project.pk)
        except User.DoesNotExist as n:
            return render(request, self.template_name, {"project": project, "error": n})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_obj"
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = Project.objects.filter(users__username__icontains=self.object.username)
        paginator = Paginator(projects, self.paginate_related_by,
                              orphans=self.paginate_related_orphans)
        page_num = self.request.GET.get("page", 1)
        page = paginator.get_page(page_num)
        kwargs["page_obj"] = page
        kwargs["project_list"] = page.object_list
        kwargs["is_paginated"] = page.has_other_pages()
        return super().get_context_data(**kwargs)
