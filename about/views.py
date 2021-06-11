from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Representation of a static page about the author."""
    template_name = 'misc/about_author.html'


class AboutTechView(TemplateView):
    """Static Technology Page View."""
    template_name = 'misc/about_tech.html'
