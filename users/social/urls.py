from django.urls import path, include
from .views import RestfulOAuth2CallbackView
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
]

urlpatterns = [
    path('login/', include(social_providers)),
]

