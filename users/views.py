from django.shortcuts import render
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

