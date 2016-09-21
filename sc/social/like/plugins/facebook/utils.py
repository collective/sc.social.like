# -*- coding:utf-8 -*-
from config import FB_LOCALES


def fix_iso(code):
    # TODO: We should be dealing also with *simple*
    #      language codes like pt or en or es
    if code.find('-') > -1:
        # we have a iso code like pt-br and FB_LOCALES uses pt_BR
        code = code.split('-')
        code = '{0}_{1}'.format(code[0], code[1].upper())
        # Deal with Umbrella locations (Arabic and Spanish)
        if code.startswith('es_'):
            if code not in FB_LOCALES:
                code = 'es_LA'
        elif code.startswith('ar_'):
            code = 'ar_AR'
    elif code.find('_') == -1:
        # XXX: Hack follows!
        # Try to find the best combination...
        available = [fb for fb in FB_LOCALES if fb.startswith(code)]
        if len(available) == 1:
            # Just one match, use it
            code = available[0]
        elif len(available) > 1:
            # We have several choices...
            # try to find a xx_XX combination if possible.
            # if not, return the first one..
            if '{0}_{1}'.format(code.lower(), code.upper()) in FB_LOCALES:
                code = '{0}_{1}'.format(code.lower(), code.upper())
            else:
                code = available[0]
    return code


def facebook_language(languages, default):
    """Given the prefered language on request we return the right
    language_code option to the template
    """
    if not languages:
        # do not change anything
        return default
    languages = [languages, ] if not isinstance(languages, list) else languages
    languages = [fix_iso(l) for l in languages]
    prefered = [l for l in languages if l in FB_LOCALES]
    return prefered and prefered[0] or default
