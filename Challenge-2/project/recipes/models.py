from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ingredient(TimeStampModel):
    name = models.CharField(verbose_name=_('ingredient name'), max_length=100, unique=True)
    quantity = models.FloatField(verbose_name=_('quantity'), default=0)
    unit = models.CharField(verbose_name=_('unit'), max_length=50)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
