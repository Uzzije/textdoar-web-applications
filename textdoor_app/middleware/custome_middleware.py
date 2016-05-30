from django.core.urlresolvers import reverse
from django.http import Http404


class RestrictStaffToAdminMiddleware(object):
    """
    A textdoor_app that restricts staff members access to administration panels. Author
    http://stackoverflow.com/users/313827/ip
    """

    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated():
                if not request.user.is_staff or not request.user.is_superuser:
                    raise Http404
            else:
                raise Http404