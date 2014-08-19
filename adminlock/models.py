from datetime import timedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from .conf import MAX_LOCK_TIME


class UserLock(models.Model):
    """Lock object by user"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey('content_type', 'object_pk')

    class Meta:
        verbose_name = _('User lock')
        verbose_name_plural = _('User locks')

    @property
    def unlock_time(self):
        """return time that this lock will be unlocked"""
        return self.create_at + timedelta(seconds=MAX_LOCK_TIME)

