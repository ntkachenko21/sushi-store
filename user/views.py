from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import login
from django.views import View
from django_htmx.http import HttpResponseClientRefresh

from user.forms import CustomUserCreationForm, CustomLoginForm
from user.models import CustomUser


class LoginModalView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(
            request, "includes/modals/login_modal.html", {"form": form}
        )

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseClientRefresh()
        return render(
            request, "includes/modals/login_modal.html", {"form": form}
        )


class SignupModalView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(
            request, "includes/modals/signup_modal.html", {"form": form}
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseClientRefresh()
        return render(
            request, "includes/modals/signup_modal.html", {"form": form}
        )


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/account.html"
    login_url = "login"

    def get_object(self):
        return self.request.user
