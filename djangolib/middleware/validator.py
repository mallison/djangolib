import json
import urllib2


class Validator(object):
    validator = 'http://html5.validator.nu/?out=json'

    def process_response(self, request, response):
        content = response.content
        req = urllib2.Request(self.validator, content)
        req.add_header('Content-type', 'text/html; charset=utf-8')
        validator_response = urllib2.urlopen(req)
        # results = json.loads(validator_response.read())
        results = validator_response.read()
        content = content.replace('</body>',
                                  results + '</body>')
        response.content = (content)
        return response
