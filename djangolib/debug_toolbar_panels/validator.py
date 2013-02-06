import json
import urllib2

from django.utils.translation import ugettext_lazy as _, ungettext_lazy as __
from debug_toolbar.panels import DebugPanel


class ValidatorDebugPanel(DebugPanel):
    """
    Panel that displays validator.nu results.
    """
    name = 'Validator'
    template = 'debug_toolbar_panels/validator.html'
    has_content = True
    validator = 'http://html5.validator.nu/?out=json'

    def nav_title(self):
        return _('Validator')

    def nav_subtitle(self):
        return __("%d validator messages",
                  "%d validator messages",
                  self._validator_messages) % self._validator_messages

    def url(self):
        return ''

    def title(self):
        return _('Validator')

    def process_response(self, request, response):
        content = response.content
        req = urllib2.Request(self.validator, content)
        req.add_header('Content-type', 'text/html; charset=utf-8')
        validator_response = urllib2.urlopen(req)
        results = json.loads(validator_response.read())
        self.context['validator_results'] = results
        self._validator_messages = len(results['messages'])
        return response
