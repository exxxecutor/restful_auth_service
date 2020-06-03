from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import allauth
from .views import (
    TokenSignupView,
    ProfileView,
    LogoutView,
    ChangePasswordView,
)

from allauth.account.views import confirm_email

password_urls = [
    path('change/', ChangePasswordView.as_view(), name='change_password'),
    #todo
    #  should be restful version of the same allauth view.
    #  must make a reset link and send it via mail
    # path('reset/',),
]

# These views are not from DjangoRESTfr.!
# These are for compatibility ...
# Do not change names!
regular_views = [
    # link that is sent via mail on every reset request
    # should display a change pass form and be one time link
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            allauth.account.views.password_reset_from_key,
            name="account_reset_password_from_key"),
    # used on signup
    # works on GET (which is fine imho)
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", confirm_email,
            name="account_confirm_email"),
]

urlpatterns = [
    path('signup/', TokenSignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # todo patch profile info
    path('profile/', ProfileView.as_view(), name='profile'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/', include(password_urls)),
    # social providers using django-allauth
    path('social/', include('users.social.urls')),
]

urlpatterns += regular_views
