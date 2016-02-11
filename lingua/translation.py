from django.db.models import signals
import handler
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.translation import activate, deactivate
from django.db import models

signals.post_init.connect(handler.post_init)


class TranslationModel(models.Model):
    def __init__(self, *args, **kwargs):

        _languages = dict(filter(lambda x: x[0] != getattr(settings, 'LINGUA_DEFAULT', 'en'),
                                 getattr(settings, 'LANGUAGES', ())))
        translation_fields = tuple([x for x in [x.lower() for x in self._translation_fields if '__' not in x]])

        def _getattr(klass, name):
            if '_' in name:
                lang, v = name.split('_')[::-1][0], '_'.join(name.split('_')[:-1])

                if lang in _languages:
                    activate(lang)
                    value = unicode(_(getattr(klass, v)))
                    deactivate()

                    return value
            return klass.__class__.__getattribute__(klass, name)

        self.__class__.add_to_class('_translation_fields', translation_fields)
        self.__class__.add_to_class('_languages', _languages)
        self.__class__.add_to_class('__getattr__', _getattr)

        super(TranslationModel, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True
