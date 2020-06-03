from allauth.socialaccount.providers.oauth2.views import OAuth2View
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RestfulOAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if 'code' not in request.query_params:
            return Response({
                'detail': "'code' query parameter is not provided"
            }, status.HTTP_400_BAD_REQUEST)

        app = self.adapter.get_provider().get_app(self.request)
        client = self.get_client(request, app)
        try:
            access_token = client.get_access_token(request.query_params['code'])
            token = self.adapter.parse_token(access_token)
            token.app = app
            login = self.adapter.complete_login(request,
                                                app,
                                                token,
                                                response=access_token)
            login.token = token
            # checks if account already exist
            login.lookup()
            # if not - saves user instance, social account
            if not login.is_existing:
                # dummy session bcs it tries to cache
                request.session = {}
                login.save(request)

            refresh = RefreshToken.for_user(login.user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:  # PermissionDenied, OAuth2Error, RequestException, ProviderException
            return Response({
                "detail": e.args,
            }, status=status.HTTP_400_BAD_REQUEST)


class SocialLoginTestView(TemplateView):
    template_name = 'test/social.html'

