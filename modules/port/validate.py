#!/usr/bin/env python
"""
validate.py - casca Validation Module
Copyright 2009-2013, Michael Yanovich (yanovich.net)
Copyright 2008-2013, Sean B. Palmer (inamidst.com)
Licensed under the Eiffel Forum License 2.

More info:
 * casca: https://github.com/myano/casca/
 * Casca: http://github.com/faxalter/casca/
"""

import web

def val(casca, input):
    """Check a webpage using the W3C Markup Validator."""
    if not input.group(2):
        return casca.reply("Nothing to validate.")
    uri = input.group(2)
    if not uri.startswith('http://'):
        uri = 'http://' + uri

    path = '/check?uri=%s;output=xml' % web.urllib.quote(uri)
    info = web.head('http://validator.w3.org' + path)

    result = uri + ' is '

    if isinstance(info, list):
        return casca.say('Got HTTP response %s' % info[1])

    if info.has_key('X-W3C-Validator-Status'):
        result += str(info['X-W3C-Validator-Status'])
        if info['X-W3C-Validator-Status'] != 'Valid':
            if info.has_key('X-W3C-Validator-Errors'):
                n = int(info['X-W3C-Validator-Errors'].split(' ')[0])
                if n != 1:
                    result += ' (%s errors)' % n
                else: result += ' (%s error)' % n
    else: result += 'Unvalidatable: no X-W3C-Validator-Status'

    casca.reply(result)
val.rule = (['val'], r'(?i)(\S+)')
val.example = '.val http://www.w3.org/'

if __name__ == '__main__':
    print __doc__.strip()
