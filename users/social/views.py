from allauth.socialaccount.providers.oauth2.views import OAuth2View


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
            # if self.adapter.supports_state:
            #     login.state = SocialLogin \
            #         .verify_and_unstash_state(
            #         request,
            #         get_request_param(request, 'state'))
            # else:
            #     login.state = SocialLogin.unstash_state(request)
            return complete_social_login(request, login)
        except (PermissionDenied,
                OAuth2Error,
                RequestException,
                ProviderException) as e:
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                exception=e)