==============
Django Lingua
==============

This is a i18n for the database on the basis of gettext

Reduce the database hits to 0

* Translate it directly in the admin interface
* Access the translation to each field to each language 

Compatible Django >= 1.9
Should work for previous version of Django, not tested yet.


TODO:
Find a way to mixin the model without using a mixin model.
Maybe use `contribute_class` as used before.
