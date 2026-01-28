from rest_framework.throttling import SimpleRateThrottle

class EmailVerificationThrottle(SimpleRateThrottle):
    scope = 'email_verification'

    def get_cache_key(self, request, view):
        email = request.data.get('email')
        if not email:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': email
        }
