from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'misc/about_author.html'


class AboutTechView(TemplateView):
    template_name = 'misc/about_tech.html'
