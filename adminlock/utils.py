from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from .models import UserLock
from .conf import MAX_LOCK_TIME


def check_lock(obj):
    """
    return :class:`adminlock.models.UserLock` object if obj is locked for edit
    return `None` if there is no lock
    """
    now_lock = now() - timedelta(seconds=MAX_LOCK_TIME)
    content_type = ContentType.objects.get_for_model(obj.__class__)

    try:
        user_lock = UserLock.objects.get(
            content_type=content_type,
            object_pk=obj.pk,
            create_at__gte=now_lock)
    except UserLock.DoesNotExist:
        return None
    else:
        return user_lock


def make_lock(obj, user):
    """
    make lock for obj and user
    """
    content_type = ContentType.objects.get_for_model(obj.__class__)
    UserLock.objects.create(
        content_type=content_type,
        object_pk=obj.pk,
        user=user
    )
