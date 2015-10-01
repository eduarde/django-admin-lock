from django.contrib import admin
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _now
from django.utils.encoding import force_text
from .models import UserLock
from .utils import check_lock, make_lock

class AdminLockMixIn(object):
    """
    MixIn class allow to mix it with other admin classes if you want to make sure
    that data edit in admin are not g
    """
    def change_view(self, request, object_id, form_url='', extra_context=None):

        # check if view is not locked for this user
        obj = self.get_object(request, unquote(object_id))
        user_lock = check_lock(obj)
        if user_lock and user_lock.user != request.user:
            # object is locked, display proper message
            return self.render_user_lock(request, user_lock, obj)

        response = super(AdminLock, self).change_view(
            request, object_id, form_url, extra_context)

        # lock object for current user if there is no user_lock
        if not user_lock:
            make_lock(obj, request.user)

        return response

    def render_user_lock(self, request, user_lock, obj):
        """return user lock screen"""
        model = self.model
        opts = model._meta

        # check if user has permision do unlock object
        force_unlock = request.user.has_perm('adminlock.delete_userlock')

        context = {
            'user_lock': user_lock,
            'obj': obj,
            'app_label': opts.app_label,
            'title': _now('Lock %s') % force_text(opts.verbose_name),
            'object_id': obj.pk,
            'original': obj,
            'opts': opts,
            'force_unlock': force_unlock
        }

        return TemplateResponse(
            request,
            "admin/user_lock.html",
            context,
            current_app=self.admin_site.name)


class AdminLock(admin.ModelAdmin, AdminLockMixIn):
    """
    AdminLock class. Prevent from editing form by two users in same time
    """
    pass


class UserLockAdmin(admin.ModelAdmin):
    """classic User Lock admin to control locking from backoffice"""

    list_display = ('object_pk', 'content_type', 'user', 'create_at')

    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        obj = self.get_object(request, unquote(object_id))
        response = super(UserLockAdmin, self).delete_view(
            request, object_id, extra_context)
        if request.POST:
            return HttpResponseRedirect(
                reverse(
                    'admin:%s_%s_change' % (obj.content_type.app_label,
                                            obj.content_type.model),
                    args=(obj.object_pk,)))
        return response

admin.site.register(UserLock, UserLockAdmin)
