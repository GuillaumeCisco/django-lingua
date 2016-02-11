from django.core.management import BaseCommand, CommandError
from django.utils.encoding import smart_str
from django.apps import apps
from django.db import models, router, connections, DEFAULT_DB_ALIAS
from collections import OrderedDict
from django.utils.translation.trans_real import all_locale_paths, check_for_language, language_code_re, to_locale
import gettext as gettext_module
import os
from django.core.files import File


class Command(BaseCommand):
    help = "Translate database messages"

    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument('--database', action='store', dest='database',
                            default=DEFAULT_DB_ALIAS, help='Nominates a database to synchronize. '
                                                           'Defaults to the "default" database.')

    def handle(self, *args, **options):
        db_values = []
        db = options.get('database')
        connection = connections[db]
        connection.prepare_database()

        # Build the manifest of apps and models that are to be synchronized
        all_models = [
            (app_config.label,
             router.get_migratable_models(app_config, connection.alias, include_auto_created=False))
            for app_config in apps.get_app_configs()
            ]

        for app_name, model_list in all_models:
            for m in model_list:
                if hasattr(m, '_translation_fields'):
                    for x in m._translation_fields:
                        for y in m.objects.all():
                            db_values.append(getattr(y, x))

                    path = apps.app_configs[app_name].path
                    # print db_values
                    with open(os.path.join(path, 'extra_translations.py'), 'w') as f:
                        translations_file = File(f)
                        translations_file.write('''# encoding: utf-8

from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _

translations = (
''')
                        for v in db_values:
                            translations_file.write("""    _('%s'),\n""" % smart_str(v.replace('\'', '\\\'')))
                        translations_file.write(')')
