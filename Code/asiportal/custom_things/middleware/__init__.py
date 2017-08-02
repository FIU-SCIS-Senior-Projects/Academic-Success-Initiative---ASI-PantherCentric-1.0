from django.core.exceptions import SuspiciousOperation
from django.views.defaults import server_error

class SquashInvalidHostMiddleware(object):
    def process_request(self, request):
        try:
            request.get_host()
        except SuspiciousOperation:
            return server_error(request)
