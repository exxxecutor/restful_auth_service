from allauth.socialaccount.providers.oauth2.views import OAuth2View
from django.views.generic import TemplateView
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RestfulOAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        for required_parameter in ['code', 'process']:
            if required_parameter not in request.query_params:
                return Response({
                    'detail': f"'{required_parameter}' query parameter is not provided"
                }, status.HTTP_400_BAD_REQUEST)

        process = request.query_params['process']
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
        except Exception as e:  # PermissionDenied, OAuth2Error, RequestException, ProviderException
            return Response({
                "detail": e.args,
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            handler = getattr(self, process.lower())
        except AttributeError:
            return Response({
                'detail': f'Process "{process}" is not supported'
            }, status=status.HTTP_400_BAD_REQUEST)

        return handler(request, *args, login=login, **kwargs)

    def connect(self, request, *, login):
        if request.user.is_anonymous:
            if request.auth:
                raise NotAuthenticated("Access token is invalid or outdated")
            raise NotAuthenticated()
        # checks if social account already exist
        # if so, also gets the user it is associated with
        login.lookup()
        if login.is_existing:
            return Response({
                "detail": "This account is already connected to another user"
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            login.connect(request, request.user)

        return Response(status=status.HTTP_201_CREATED)

    def login(self, request, *, login):
        login.lookup()
        if not login.is_existing:
            login.save(request)

        refresh = RefreshToken.for_user(login.user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class SocialLoginTestView(TemplateView):
    template_name = 'test/social_connect.html'


class SocialDisconnectView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        if 'provider' not in request.query_params:
            return Response({
                'detail': '"provider" parameter is missing'
            }, status=status.HTTP_400_BAD_REQUEST)

        social_accounts = \
            request.user.socialaccount_set.filter(provider=request.query_params['provider']).all()

        if social_accounts:
            for account in social_accounts:
                account.delete()

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)



