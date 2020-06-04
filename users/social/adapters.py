from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from allauth.utils import build_absolute_uri
from django.urls import reverse

SOCIAL_LOGIN_CALLBACK_NAME = 'social_login_callback'


# how else can i redefine every adapter's method?
class GoogleAdapter(GoogleOAuth2Adapter):
    def get_callback_url(self, request, app):
        assert 'process' in request.query_params
        callback_url = reverse(SOCIAL_LOGIN_CALLBACK_NAME)
        protocol = self.redirect_uri_protocol
        url = build_absolute_uri(request, callback_url, protocol)
        return url + f'?process={request.query_params["process"]}&provider={self.provider_id}'


class FacebookAdapter(FacebookOAuth2Adapter):
    def get_callback_url(self, request, app):
        assert 'process' in request.query_params
        callback_url = reverse(SOCIAL_LOGIN_CALLBACK_NAME)
        protocol = self.redirect_uri_protocol
        url = build_absolute_uri(request, callback_url, protocol)
        return url + f'?process={request.query_params["process"]}&provider={self.provider_id}'


class DiscordAdapter(DiscordOAuth2Adapter):
    def get_callback_url(self, request, app):
        assert 'process' in request.query_params
        callback_url = reverse(SOCIAL_LOGIN_CALLBACK_NAME)
        protocol = self.redirect_uri_protocol
        url = build_absolute_uri(request, callback_url, protocol)
        return url + f'?provider={self.provider_id}&process={request.query_params["process"]}'
