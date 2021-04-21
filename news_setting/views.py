from django.shortcuts import render
from django.views.generic import View
from .models import AboutUs


# Create your views here.
class AboutUsView( View ):
    template_name = 'settings/about_us_page.html'

    def get(self, request):
        about_us = AboutUs.objects.last()
        context = {
            'title': 'درباره ما',
            'about_us': about_us
        }
        return render( request, self.template_name, context )
