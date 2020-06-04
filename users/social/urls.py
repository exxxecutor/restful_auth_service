from django.urls import path, include
from .views import (
    RestfulOAuth2CallbackView,
    SocialLoginTestView,
    SocialDisconnectView,
)
from .adapters import (
    FacebookAdapter,
    GoogleAdapter,
    DiscordAdapter,
)
from rest_framework.decorators import api_view

# TODO separate namespace "social"
# TODO new account with the existing username creation via social login
urlpatterns = [
    path('google/',
         api_view(http_method_names=['POST'])(RestfulOAuth2CallbackView.adapter_view(GoogleAdapter)),
         name='google_login'),
    path('facebook/',
         api_view(http_method_names=['POST'])(RestfulOAuth2CallbackView.adapter_view(FacebookAdapter)),
         name='facebook_login'),
    path('discord/',
         api_view(http_method_names=['POST'])(RestfulOAuth2CallbackView.adapter_view(DiscordAdapter)),
         name='discord_login'),
    path('disconnect/', SocialDisconnectView.as_view(), name='disconnect'),
    # to_delete, used for social login testing, replaces front-end web app part
    path('test/', SocialLoginTestView.as_view(), name='social_login_callback'),
]

