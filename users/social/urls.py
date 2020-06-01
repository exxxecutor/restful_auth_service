from django.urls import path, include
from .views import RestfulOAuth2CallbackView, SocialLoginTestView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.decorators import api_view

social_providers = [
    path('google/',
         api_view(http_method_names=['GET'])(RestfulOAuth2CallbackView.adapter_view(GoogleOAuth2Adapter)),
         name='google_login'),
    path('facebook/',
         api_view(http_method_names=['GET'])(RestfulOAuth2CallbackView.adapter_view(FacebookOAuth2Adapter)),
         name='facebook_login'),
    # to_delete, used for social login testing, replaces front-end web app part
    path('google/test', SocialLoginTestView.as_view()),
    path('facebook/test', SocialLoginTestView.as_view()),
]

urlpatterns = [
    path('login/', include(social_providers)),
]

