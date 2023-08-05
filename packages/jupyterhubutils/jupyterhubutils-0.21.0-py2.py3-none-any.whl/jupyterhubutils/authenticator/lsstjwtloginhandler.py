'''LSST Login Handler to use JWT token present in request headers.
'''
import datetime
from eliot import start_action
from tornado import gen, web
from jupyterhub.utils import url_path_join
from jwtauthenticator.jwtauthenticator import JSONWebTokenLoginHandler
from ..lsstmgr import check_membership


class LSSTJWTLoginHandler(JSONWebTokenLoginHandler):

    @gen.coroutine
    def get(self):
        '''Authenticate on get() via reading the token from HTTP headers.
        '''
        # This causes some token context error in Eliot
        # with start_action(action_type="get"):
        _ = yield self._jwt_authenticate()
        #
        # We can't just use the superclass because it issues the redirect,
        #  and we can't do that until we do our additional checking.
        _url = url_path_join(self.hub.server.base_url, 'home')
        next_url = self.get_argument('next', default=False)
        if next_url:
            _url = next_url
        self.redirect(_url)

    @gen.coroutine
    def post(self):
        '''Also authenticate on POST, if necessary.'''
        with start_action(action_type="post"):
            _ = yield(self._jwt_authenticate())
            yield super().post()

    @gen.coroutine
    def _jwt_authenticate(self):
        # This is taken from https://github.com/mogthesprog/jwtauthenticator
        #  but with our additional claim information checked and stuffed
        #  into auth_state, and allow/deny lists checked.
        # Context problem here too.
        # with start_action(action_type="_jwt_authenticate"):
        claims, token = yield self._check_auth_header()
        username_claim_field = self.authenticator.username_claim_field
        username = self.retrieve_username(claims, username_claim_field).lower()
        user = self.user_from_username(username)
        # Here is where we deviate from the vanilla JWT authenticator.
        # We simply store all the JWT claims in auth_state, although we
        #  choose our field names to make the spawner reusable from the
        #  OAuthenticator implementation.
        auth_state = yield self.refresh_user(user)
        if not self._jwt_validate_user(auth_state):
            # We're either in a forbidden group, or in no allowed groups
            self.log.error("User did not validate from claims groups.")
            raise web.HTTPError(403)
        _ = yield user.save_auth_state(auth_state)
        self.set_login_cookie(user)

    @gen.coroutine
    def refresh_user(self, user, handler=None):
        '''Validate the token and force re-auth if the claims are not
        (presumably no longer) valid.
        '''
        with start_action(action_type="refresh_user"):
            self.log.debug("Refreshing user data.")
            try:
                claims, token = yield self._check_auth_header()
            except web.HTTPError:
                # Force re-login
                return False
            username_claim_field = self.authenticator.username_claim_field
            username = self.retrieve_username(
                claims, username_claim_field).lower()
            auth_state = {"id": username,
                          "access_token": token,
                          "claims": claims}
            return auth_state

    @gen.coroutine
    def _check_auth_header(self):
        with start_action(action_type="_check_auth_header"):
            # Either returns (valid) claims and token,
            #  or throws a web error of some type.
            self.log.debug("Checking authentication header.")
            auth = self.authenticator
            cfg = auth.lsst_mgr.config
            header_name = auth.header_name
            param_name = auth.param_name
            header_is_authorization = auth.header_is_authorization
            auth_header_content = self.request.headers.get(header_name, "")
            auth_cookie_content = self.get_cookie("XSRF-TOKEN", "")
            signing_certificate = cfg.jwt_signing_certificate
            secret = auth.secret
            audience = cfg.audience
            tokenParam = self.get_argument(param_name, default=False)
            if auth_header_content and tokenParam:
                self.log.error("Authentication: both an authentication " +
                               "header and tokenParam")
                raise web.HTTPError(400)
            elif auth_header_content:
                if header_is_authorization:
                    # We should not see "token" as first word in the
                    #  authorization header.  If we do it could mean someone
                    #  coming in with a stale API token
                    if auth_header_content.split()[0].lower() != "bearer":
                        self.log.error("Authorization header is not 'bearer'.")
                        raise web.HTTPError(403)
                    token = auth_header_content.split()[1]
                else:
                    token = auth_header_content
            elif auth_cookie_content:
                token = auth_cookie_content
            elif tokenParam:
                token = tokenParam
            else:
                self.log.error("Could not determine authentication token.")
                raise web.HTTPError(401)
            claims = ""
            if secret:
                claims = self.verify_jwt_using_secret(token, secret, audience)
            elif signing_certificate:
                claims = self.verify_jwt_with_claims(token,
                                                     signing_certificate,
                                                     audience)
            else:
                self.log.error("Could not verify JWT.")
                raise web.HTTPError(401)
            # Check expiration
            expiry = int(claims['exp'])
            now = int(datetime.datetime.utcnow().timestamp())
            if now > expiry:
                self.log.error("JWT has expired!")
                raise web.HTTPError(401)
            auth.token = token
            return claims, token

    def _jwt_validate_user(self, auth_state):
        with start_action(action_type="_jwt_validate_user"):
            cfg = self.authenticator.lsst_mgr.config
            claims = auth_state['claims']
            uid, groupmap = self.authenticator.resolve_cilogon(claims)
            groups = list(groupmap.keys())
            valid = check_membership(
                groups, cfg.allowed_groups, cfg.forbidden_groups, log=self.log)
            if not valid:
                self.log.warning("Group membership check failed.")
                return False
            auth_state['group_map'] = groupmap
            auth_state['uid'] = uid
            return True
