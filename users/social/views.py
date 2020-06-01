from allauth.socialaccount.providers.oauth2.views import OAuth2View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class RestfulOAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if 'error' in request.GET or 'code' not in request.GET:
            # # Distinguish cancel from error
            # auth_error = request.GET.get('error', None)
            # if auth_error == self.adapter.login_cancelled_error:
            #     error = AuthError.CANCELLED
            # else:
            #     error = AuthError.UNKNOWN
            # todo handle error
            pass
        app = self.adapter.get_provider().get_app(self.request)
        client = self.get_client(request, app)
        try:
            access_token = client.get_access_token(request.GET['code'])
            token = self.adapter.parse_token(access_token)
            token.app = app
            login = self.adapter.complete_login(request,
                                                app,
                                                token,
                                                response=access_token)
            login.token = token
            # saves user instance, social account
            login.save()
            refresh = RefreshToken.for_user(login.user)
            # if self.adapter.supports_state:
            #     login.state = SocialLogin \
            #         .verify_and_unstash_state(
            #         request,
            #         get_request_param(request, 'state'))
            # else:
            #     login.state = SocialLogin.unstash_state(request)
            # todo return access and refresh token
            return Response({
                'refresh': refresh,
                'access': refresh.access,
            })
        except Exception as e:  # PermissionDenied, OAuth2Error, RequestException, ProviderException
            return Response({
                "detail": e.args,
            }, status=status.HTTP_409_CONFLICT)


class SocialLoginTestView(TemplateView):
    template_name = 'test/social.html'
