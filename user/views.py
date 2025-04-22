from django.contrib.auth.views import LoginView
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
        return render(request, "includes/modals/login_modal.html", {"form": form})

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseClientRefresh()
        return render(request, "includes/modals/login_modal.html", {"form": form})


class CustomRegisterView(CreateView):
    template_name = 'product/index.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('product:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            show_signup_modal=True
        ))

class SignupModalView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "includes/modals/signup_modal.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseClientRefresh()
        return render(request, "includes/modals/signup_modal.html", {"form": form})


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/account.html'
    login_url = 'login'

    def get_object(self):
        return self.request.user
