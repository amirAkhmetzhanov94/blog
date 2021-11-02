from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.views.generic import View, CreateView, DetailView, ListView, UpdateView
from django.http import HttpResponseRedirect
from accounts.forms import RegistrationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm
from accounts.models import Profile
from webapp.models import Project
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import MultipleObjectMixin


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
        Profile.objects.create(user=user)
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


class UserDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_obj"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        object_list = Project.objects.filter(users__username__icontains=self.object.username)
        context = super(UserDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class UserListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = "users_list.html"
    context_object_name = "users_list"
    paginate_by = 10
    permission_required = "accounts.view_profile"


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "edit_profile.html"
    context_object_name = "user_obj"

    def test_func(self):
        return self.request.user == self.get_object() or \
               self.request.user.is_superuser or self.request.user.groups.filter(name="admins")

    def get_profile_form(self):
        form_kwargs = {"instance": self.object.profile}
        if self.request.method == "POST":
            form_kwargs["data"] = self.request.POST
            form_kwargs["files"] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        result = super().form_valid(user_form)
        profile_form.save()
        return result

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = self.get_profile_form()
            kwargs["user_form"] = self.get_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.object.pk})


class ChangePasswordView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    context_object_name = "user_obj"

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.instance)
        return redirect("accounts:profile", pk=self.get_object().pk)

    def test_func(self):
        return self.request.user == self.get_object() or \
               self.request.user.is_superuser or self.request.user.groups.filter(name="admins")