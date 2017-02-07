from django.contrib.sites.models import Site


def site(request):
    site = Site.objects.get_current()
    return {
        'sitio': site,
        'dominioIglesia': site.domain,
        'nombreIglesia': site.name
    }
