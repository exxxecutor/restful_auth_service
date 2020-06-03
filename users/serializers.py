from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django import forms
from .models import CustomUser
from allauth.account.models import EmailAddress
from django.contrib.auth.forms import UserCreationForm, UsernameField
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField()

    def save(self, commit=True):
        user = super().save(commit)
        user_email = EmailAddress(user=user, email=self.cleaned_data['email'])
        user_email.send_confirmation()
        user_email.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('username',)
        field_classes = {
            'username': UsernameField
        }


class TokenSignupSerializer(serializers.Serializer):

    def validate(self, attrs):
        """
        Validate the input, saves user if valid
        :param attrs:
        :raises AuthenticationFailed: If data is not valid
        :return: refresh access tokens
        """
        user_form = \
            CustomUserCreationForm(self.initial_data)

        if user_form.is_valid():
            user = user_form.save(commit=True)
        else:
            raise AuthenticationFailed(user_form.errors)

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']
