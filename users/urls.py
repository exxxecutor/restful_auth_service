from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    TokenSignupView,
    ProfileView,
    LogoutView,
    # SocailLoginView,
)

from allauth.account.views import confirm_email

urlpatterns = [
    path('signup/', TokenSignupView.as_view(), name='signup'),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", confirm_email,
            name="account_confirm_email"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # social providers using django-allauth
    path('social/', include('users.social.urls')),
]
