from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from .serializers import (
    TokenSignupSerializer,
    ProfileSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from allauth.account.forms import ResetPasswordForm


class TokenSignupView(TokenViewBase):
    serializer_class = TokenSignupSerializer


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Return user's profile info
        :param request:
        :return:
        """
        profile = ProfileSerializer(request.user)
        return Response(profile.data)
        # else:
        #     # not sure about the status code and error msg in overall
        #     # is there any errors that can be?
        #     # maybe the user is inactive or email isn't confirmed?
        #     return Response(profile.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if 'refresh' not in request.data:
            # todo raise approp error
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)
        token = RefreshToken(request.data['refresh'])
        token.blacklist()
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(APIView):

    def post(self, request):
        try:
            assert 'email' in request.data
            form = ResetPasswordForm(request.data)
            if form.is_valid():
                form.save()
            else:
                raise ValidationError("Invalid email address")

        except AssertionError:
            return Response({
                'detail': "'email' field is not provided"
            }, status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    authentication_classes = (IsAuthenticated,)

    def post(self, request):
        if 'password' not in request:
            return Response({
                'detail': "'password' is not provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.user.check_password(request.data['password']):
            request.user.set_password(request.data['password'])
            return Response()
        else:
            return ValidationError("passwords didn't match")
