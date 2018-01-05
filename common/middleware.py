'''
Middlewares compatibles for version 1.11+ of django.
'''

from waffle import middleware


class WaffleMiddleWareCompat(middleware.WaffleMiddleware):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)
