from django.utils.translation import trans_real, activate
import gettext


def clear_gettext_cache():
    gettext._translations = {}
    trans_real._translations = {}
    trans_real._default = None
    prev = trans_real.get_language()
    if prev:
        activate(prev)
