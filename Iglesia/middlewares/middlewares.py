from django.http import HttpResponseRedirect
from django.conf import settings

class Middleware(object):
	def process_request(self, request):
		pass

	def process_response(self, request, response):
		try:
			# Se verifica si es una redireccion o si se ha escrito directamente en la url
			# print(len(request.POST))
			user = request.user
			if user.is_authenticated():
				if len(request.POST) == 0 and len(request.GET) == 0:
					if request.path != settings.LOGIN_URL and response.status_code == 302:
						print("No tiene Permisos")
						return HttpResponseRedirect('/dont_have_permissions/')
					return response
			return response

		except AttributeError:
			print("Error")
			return response
