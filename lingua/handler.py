from django.utils.translation import ugettext_lazy as _


def post_init(sender, instance, **kwargs):
    """Class is ready, all attributes has been set """
    """Loop through translation fields and set the gettext in beetween """
    if hasattr(sender, '_translation_fields'):
        for x in sender._translation_fields:
            value = getattr(instance, x)
            setattr(instance, x, _(value))
            setattr(instance, "_".join((x,"00")), value)#original value
