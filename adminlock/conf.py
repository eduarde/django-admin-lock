from django.conf import settings

# max lock time in seconds.
# after this time object is automaticly unlocked
MAX_LOCK_TIME = getattr(settings, 'ADMINLOCK_MAX_LOCK_TIME', 60*30)