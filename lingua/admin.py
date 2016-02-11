from django.contrib import admin
import os
import polib
from django.apps import apps


class LinguaModelAdmin(admin.ModelAdmin):

    @staticmethod
    def get_fields_with_type(model, fields_type):
        fields = []
        for field in model._translation_fields:
            for l in model._languages.keys():
                name = '_'.join((field, l))
                field_type = fields_type[field]
                fields.append( (name, field_type.__class__(widget=field_type.widget) ) )
        return fields

    @staticmethod
    def get_admin_fields(request, obj=None):
        return ['_'.join((field, l)) for field in obj._translation_fields for l in obj._languages.keys()]


    def get_form(self, request, obj=None, **kwargs):
        kwargs['fields'] = None
        form = super(LinguaModelAdmin, self).get_form(request, obj, **kwargs)
        
        class LinguaAdminForm(form):
            def __init__(self, *args, **kwargs):
                super(LinguaAdminForm, self).__init__(*args, **kwargs)

                instance = kwargs.get("instance", None)

                fields_type = dict([(x, self.fields[x]) for x in self._meta.model._translation_fields])
                fields = LinguaModelAdmin.get_fields_with_type(self._meta.model, fields_type)

                #create fields dynamically
                for x, y in fields:
                    self.fields[x] = y

                #make sure the original value will be shown
                for x in self._meta.model._translation_fields:
                    self.initial[x] = instance and getattr(instance, "_".join( (x,'00') )) or ""

                initial = instance and dict( [ (x, getattr(instance, x)) for x,y in fields] ) or {}

                self.initial.update(initial)

            def save(self, *args, **kwargs):
                model = super(LinguaAdminForm, self).save(*args, **kwargs)
                from django.conf import settings
                from lingua.utils import clear_gettext_cache

                if model._meta.app_label:
                    self.projectpath = os.path.join(apps.app_configs[model._meta.app_label].path, 'locale')
                    self.languages_po = {}
                    for l in dict(settings.LANGUAGES).keys():
                        p = os.path.join(self.projectpath, l, 'LC_MESSAGES', 'django.po')
                        if os.path.exists(p):                   
                            self.languages_po[l] = polib.pofile(p)

                for f in model._translation_fields:
                    for l in model._languages:
                        field = "_".join((f,l))
                        msgid = self.cleaned_data.get(f, None)
                        c = self.cleaned_data.get(field, None)
                        if l in self.languages_po:
                            po = self.languages_po[l]
                            po_entry = po.find(msgid)
                            if po_entry:
                                po_entry.msgstr = c
                            else:
                                entry = polib.POEntry(msgid=msgid, msgstr=c)
                                po.append(entry)

                for k, p in self.languages_po.items():
                    p.save()
                    path = os.path.join(self.projectpath, k, 'LC_MESSAGES', 'django.mo')
                    p.save_as_mofile(path)

                #reset gettext cache
                clear_gettext_cache()

                return model

        return LinguaAdminForm

    def get_fieldsets(self, request, obj=None):
        fields = super(LinguaModelAdmin,self).get_fieldsets(request, obj)
        form = self.get_form(request, obj, fields=None)
        model = form._meta.model
        fields[0][1]["fields"] += LinguaModelAdmin.get_admin_fields(request, model)
        return fields


