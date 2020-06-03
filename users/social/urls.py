from django.urls import path, include
from .views import RestfulOAuth2CallbackView, SocialLoginTestView
from .adapter import (
    FacebookAdapter,
    GoogleAdapter,
    DiscordAdapter
)
from rest_framework.decorators import api_view

social_login_urls = [
    path('google/',
         api_view(http_method_names=['GET'])(RestfulOAuth2CallbackView.adapter_view(GoogleAdapter)),
         name='google_login'),
    path('facebook/',
         api_view(http_method_names=['GET'])(RestfulOAuth2CallbackView.adapter_view(FacebookAdapter)),
         name='facebook_login'),
    path('discord/',
         api_view(http_method_names=['GET'])(RestfulOAuth2CallbackView.adapter_view(DiscordAdapter)),
         name='facebook_login'),
    # to_delete, used for social login testing, replaces front-end web app part
    # path('google/test', SocialLoginTestView.as_view(), name='google_callback'),
    # path('facebook/test', SocialLoginTestView.as_view(), name='facebook_callback'),
    # path('discord/test', SocialLoginTestView.as_view(), name='discord_callback'),
    path('test/', SocialLoginTestView.as_view(), name='social_login_callback'),
]

# TODO
# path('connect/', include(social_connect_urls))
# social_connect_urls = [
#     path('google/', SocialConnect.as_view(adapter_cls=GoogleOAuth2Adapter)),
#     path('facebook/', SocialConnect.as_view(adapter_cls=FacebookOAuth2Adapter)),
#     path('discord/', SocialConnect.as_view(adapter_cls=DiscordOAuth2Adapter))
# ]

urlpatterns = [
    path('login/', include(social_login_urls)),
]

