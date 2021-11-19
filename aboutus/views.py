from django.views.generic import TemplateView
from .models import AboutUs as ModelAboutUs


class AboutUs(TemplateView):
    template_name = 'aboutus/about.html'
    extra_context = {
        'about': ModelAboutUs.objects.filter().first()
    }
