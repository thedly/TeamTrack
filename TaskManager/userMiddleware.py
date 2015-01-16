from TaskManager.models import ExtendedUser
from django.http import HttpResponse
from django.conf import settings
import os
import logging
log = logging.getLogger(__name__)

class SetThemeForUser(object):
    def process_request(self, request):
        log.debug("SetThemeForUser called")
        try:
            if request.user.id is not None:
                log.debug("request.user exists")
                log.debug(request.user)
                log.debug(request.user.id)
                if 'userTheme' not in request.session:
                    log.debug("userTheme does not exist")
                    userDetails = ExtendedUser.objects.get(pk=request.user.id)
                    request.session['userTheme'] = os.path.join(settings.STATIC_URL,'css/',userDetails.theme)
                    log.debug("theme is set")
                    log.debug(request.session['userTheme'])
                    return None
                else:
                    log.debug("userTheme exists")
                    return None
            else:
                log.debug("user does not exist")
                return None
        except Exception as ex:
            return HttpResponse(ex)

