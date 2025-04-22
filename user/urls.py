from django.urls import path
from django.contrib.auth.views import LogoutView
from user.views import AccountDetailView, SignupModalView, LoginModalView

urlpatterns = [
    path("login-modal/", LoginModalView.as_view(), name="login_modal"),
    path("signup-modal/", SignupModalView.as_view(), name="signup_modal"),
    path('logout/', LogoutView.as_view(next_page='product:index'), name='logout'),
    path('account/', AccountDetailView.as_view(), name='account'),
]
