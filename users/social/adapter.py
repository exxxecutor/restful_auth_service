from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter


class GoogleAdapter(GoogleOAuth2Adapter):
    def get_callback_url(self, request, app):
        """zagluwka"""
        return ""


class FacebookAdapter(FacebookOAuth2Adapter):
    def get_callback_url(self, request, app):
        """zagluwka"""
        return ""


class DiscordAdapter(DiscordOAuth2Adapter):
    def get_callback_url(self, request, app):
        """zagluwka"""
        return ""
