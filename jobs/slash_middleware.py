import os

from django import http
from django import urls
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import urlquote


def response(request, template=None, vars={}):
    if template is None:
        view_func = resolve(request.META['REQUEST_URI'])[0]
        app_label = view_func.__module__.rsplit('.', 1)[1]
        view_name = view_func.__name__
        template = '%s.html' % os.path.join(app_label, view_name)
    return render(template, vars, context=RequestContext(request))


class AppendOrRemoveSlashMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        """Returns a redirect if adding/removing a slash is appropriate. This
        works in the same way as the default APPEND_SLASH behaviour but in
        either direction."""

        urlconf = getattr(request, 'urlconf', None)
        if not _is_valid_path(request.path_info, urlconf):
            if request.path_info.endswith('/'):
                new_path = request.path_info[:-1]
            else:
                new_path = request.path_info + '/'

            if _is_valid_path(new_path, urlconf):
                return http.HttpResponsePermanentRedirect(
                    generate_url(request, new_path))

    @staticmethod
    def process_response(request, response):
        """If a 404 is raised within a view, try appending/removing the slash
        (based on the  setting) and redirecting if the new url is
        valid."""

        if response.status_code == 404:
            if not request.path_info.endswith('/') and settings.APPEND_SLASH:
                new_path = request.path_info + '/'
            elif request.path_info.endswith('/') and not settings.APPEND_SLASH:
                new_path = request.path_info[:-1]
            else:
                new_path = None

            if new_path:
                urlconf = getattr(request, 'urlconf', None)
                if _is_valid_path(new_path, urlconf):
                    return http.HttpResponsePermanentRedirect(
                        generate_url(request, new_path))
        return response


def generate_url(request, path):
    if request.get_host():
        new_url = "%s://%s%s" % (request.is_secure() and 'https' or 'http',
                                 request.get_host(),
                                 urlquote(path))
    else:
        new_url = urlquote(path)
    if request.GET:
        new_url += '?' + request.META['QUERY_STRING']
    return new_url


def _is_valid_path(path, urlconf=None):
    """
    Returns True if the given path resolves against the default URL resolver,
    False otherwise.
    """
    try:
        urls.resolve(path, urlconf)
        return True
    except urls.Resolver404:
        return False
